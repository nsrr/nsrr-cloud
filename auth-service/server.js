
const express = require('express');
const app = express();
const cors = require('cors');
const util = require('util');
const exec = util.promisify(require('child_process').exec);
const { Pool } = require('pg');
const crypto = require('crypto'); 
const jwt = require('jsonwebtoken');
const AWS = require('aws-sdk');
const fs = require('fs')

var router = express.Router();

if(process.argv.length !=2){
    console.log("Run command is node server.js")
    return
}

require('dotenv').config();

AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY,
    secretAccessKey: process.env.AWS_SECRET_KEY
  });
if (!AWS.config.region) {
    AWS.config.update({
        region: process.env.AWS_REGION
    });
} 
const s3 = new AWS.S3();

app.use(cors());
app.use(express.json());

app.listen(process.env.PORT || 9002);
console.log('Server up and running...');

var datasets_list=[]
var metadata_list=[]
var dataset_not_found_error=''
fs.readFile('hosted_datasets.txt', 'utf8' , (err, data) => {
    if (err) {
      console.error(err)
      return
    }
    metadata_list=data.split("\n")
    metadata_list.forEach(set => {
        var set_row=set.split(",")
        datasets_list.push(set_row[0])
    })
    dataset_not_found_error="Dataset was not found.\n"+
                            "Did you mean one of: "+datasets_list.join(", ")
  })

  
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_DATABASE,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
  });


  const is_valid_request = (request) =>{
    return new Promise((resolve,reject) =>{
        var client_ip=''
        console.log(request.headers['x-forwarded-for'])
        console.log(request.socket.remoteAddress)
        if(request.headers['x-forwarded-for']){
            client_ip=request.headers['x-forwarded-for'].split(",")[0]
        } else{
            if(request.socket.remoteAddress.split(":").pop()){
                client_ip=request.socket.remoteAddress.split(":").pop()
            }
        }
        if (client_ip){
            try{
                const msg="Error: service is available only from AWS cloud"
                const script ="python3 check_whitelist_ip.py "+client_ip
                async function check(){
                    try{
                        const { stdout, stderr } = await exec(script);
                        if(stderr){
                            console.error('stderr:',stderr)
                            reject (msg)
                            return
                        } else{
                            console.log(stdout.trim())
                            if(stdout.trim() == "True"){
                                resolve(client_ip)
                                return
                            } else{
                                reject(msg)
                                return
                            }
                        }
                    } catch(error){
                        reject(msg)
                        return
                    } 
                }
                check();
            }catch(error){
                reject("System error, try again later")
                return 
            }
        }
        else{
            reject("Unable to determine requestor ip-address, contact admin at support-cloud@sleepdata.org")
        }
    })
}



function generateAccessToken(payload_info) {
    return new Promise((resolve,reject) =>{
        jwt.sign({payload: payload_info}, process.env.SIGN_KEY,{expiresIn: 5}, function(err, token) {
            if(err){
                console.log("error: ",err)
                reject(false)
            } else{
                resolve(token)
            }
        });  
    })  
}

const in_maintenance_window = () =>{
    return new Promise(resolve =>{
        var date=new Date();
        while(date.getHours() == 0 && date.getMinutes()<=1){
            date=new Date();
        }
        resolve("")
    })
}

router.get('/auth-token',function(request, response,next){
    async function get_bearer_token(){
        try{
            await in_maintenance_window();
            await is_valid_request(request).then(data => {
                const requestor_ip = data
                const sleepdata_user_token = request.headers.token
                var dataset_name = request.query.dataset_name 
                if(!datasets_list.includes(dataset_name)){
                    throw new Error(dataset_not_found_error)
                }
                const user_token_split=sleepdata_user_token.split('-')
                if(user_token_split.length == 1){
                    throw new Error("Invalid token")
                }
                const user_id=user_token_split[0]
                const user_token=user_token_split.slice(1).join("-")
                const get_user_text='SELECT * from public.authn_authz where authentication_token=$1 and user_id=$2 and dataset_slug like $3'

                const get_user_fn=async function(){
                    const client = await pool.connect()
                    try{
                        client.query(get_user_text, [user_token,user_id,dataset_name+"%"],function(err,res){
                            if (err){
                                next(new Error("Server failure"))
                            }
                            else{
                                if(res.rows[0]){
                                    if(res.rows.length ==2){
                                        if(res.rows[0]["dataset_slug"].length > res.rows[1]["dataset_slug"].length ){
                                            dataset_name=res.rows[1]["dataset_slug"]
                                        } else{
                                            dataset_name=res.rows[0]["dataset_slug"]
                                        }
                                    } 
                                    if(res.rows.length==1){
                                        dataset_name=res.rows[0]["dataset_slug"]  
                                    }
                                    // process commercial version
                                    if(dataset_name.includes("commercial-use")){
                                        dataset_name=dataset_name.split("-").slice(0,-1).join("-")
                                    }
                                    //build bearer token
                                    async function get_token(){
                                        try{
                                            const payload=JSON.stringify({dataset: dataset_name})
                                            var b_token;
                                            const key = process.env.ENC_KEY;
                                            const iv= process.env.ENC_IV;
                                            var cipher = crypto.createCipheriv('aes-256-cbc', key, iv)
                                            const p1=cipher.update(payload, 'utf8');
                                            const p2=cipher.final()
                                            const payload_enc=Buffer.concat([p1, p2]).toString('hex');
                                            await generateAccessToken(payload_enc).then(data2 => b_token=data2).catch(err2 => next(err2))
                                            if(b_token){
                                                console.log("token is: ",b_token)
                                                response.status(200).send({"auth_token": b_token})
                                                // insert into pg table for audit
                                                const created_time=new Date();
                                                const token_audit_fn=async function(){
                                                    const client = await pool.connect()
                                                    try{
                                                        const token_audit_text='INSERT INTO public.bearer_token_audit( \
                                                            user_id, user_token, requested_dataset_slug, final_requested_dataset_slug, bearer_token,requestor_ip, created_at) \
                                                            VALUES ( $1, $2, $3,$4,$5,$6,$7);'
                                                        client.query(token_audit_text, [user_id, user_token,request.query.dataset_name,dataset_name,b_token,requestor_ip,created_time],function(err,res){
                                                            if (err){
                                                                console.log("System Error in inserting into token audit table")
                                                            }
                                                        })
                                                    } catch(error){
                                                        console.log("Error in inserting into token audit table")
                                                    } finally{
                                                        client.release();
                                                    }
                                                }
                                                token_audit_fn();
                                            }
                                        } catch(error){
                                            next(error)
                                        }
                                    }
                                    get_token()
                                }
                                else{
                                    console.log("Error Invalid Token")
                                    next(new Error("Invalid  Token"))
                                }
                            }
                        })
                    }catch(error){
                        console.log(error)
                        next(error)
                    }finally{
                        client.release();
                    }
                }
                get_user_fn();
            }).catch(err => {
                console.log("err is ",err)
                next(new Error("System Error, please try again"))
            })
        }catch(error){
            next(error)
        }
    }
    get_bearer_token();
})


router.get('/list/access',function(request, response,next){
    async function list_all_access(){
        try{
            await in_maintenance_window();
            await is_valid_request(request).then(data => {
                const sleepdata_user_token = request.headers.token
                const user_token_split=sleepdata_user_token.split('-')
                if(user_token_split.length == 1){
                    throw new Error("Invalid token")
                }
                const user_id=user_token_split[0]
                const user_token=user_token_split.slice(1).join("-")
                const get_user_text='SELECT dataset_slug FROM public.authn_authz where user_id=$1 and authentication_token=$2'

                var datasets_json={}
                const get_user_dbs=async function(){
                    const client = await pool.connect()
                    try{
                        client.query(get_user_text, [user_id,user_token],function(err,res){
                            if (err){
                                next(new Error("Server failure"))
                            }
                            else{
                                var datasets=[]
                                res.rows.forEach(row => {
                                    if(row["dataset_slug"].includes("-commercial-use")){
                                        datasets.push(row["dataset_slug"].split("-commercial-use")[0])      
                                    }  else{
                                        datasets.push(row["dataset_slug"])
                                    }
                                });
                                const uniq_datasets=[...new Set(datasets)];
                                datasets_json["datasets"]=uniq_datasets
                                response.status(200).send(datasets_json)

                            }
                        })
                    } catch(error){
                        next(new Error("Server failure"))
                    } finally{
                        client.release();
                    }
                }
                get_user_dbs()
            }).catch(err => {
                console.log("err is ",err)
                next(new Error(err))
            })
        } catch(error){
            next(error)
        }
    }
    list_all_access();

})


router.get('/list/all-files',function(request, response, next){
    var dataset_name= request.query.dataset_name;
    try{
        if(!datasets_list.includes(dataset_name)){
            throw new Error(dataset_not_found_error)
        }
        fs.readFile("metadata/"+dataset_name+"_metadata.json",'utf8' , (err, data) => {
            if (err) {
              next(new Error("Server Error"))
              return
            }
            var json_tosend=JSON.parse(data);
            response.status(200).send(json_tosend)
          })
    } catch(error){
        next(error)
    }
})

router.get('/list/all-subjects', function(request, response, next){
    var dataset_name= request.query.dataset_name;
    try{
        if(!datasets_list.includes(dataset_name)){
            throw new Error(dataset_not_found_error)
        }
        fs.readFile("metadata/"+dataset_name+"_all_subjects.txt",'utf8' , (err, data) => {
            if (err) {
              next(new Error("Server Error"))
              return
            }
            var json_tosend={};
            all_subjects_unfiltered=data.toString().split("\n")
            all_subjects=all_subjects_unfiltered.filter(n => n)
            json_tosend["subjects"]=all_subjects;
            response.status(200).send(json_tosend)
          })

    } catch(error){
        next(error)
    }
})

router.get('/list/subject-files', function(request, response, next){
    var dataset_name= request.query.dataset_name;
    var subject=request.query.subject
    try{
        if(!datasets_list.includes(dataset_name)){
            throw new Error(dataset_not_found_error)
        }
        fs.readFile("metadata/"+dataset_name+"_metadata_by_subject.json",'utf8' , (err, data) => {
            if (err) {
              next(new Error("Server Error"))
              return
            }
            var json_tosend={};
            all_subjects=JSON.parse(data);
            
            json_tosend=all_subjects[subject]
            console.log(json_tosend)
            response.status(200).send(json_tosend)
          })

    } catch(error){
        next(error)
    }
})

async function check_download_exists(params){
    try{
        const res=await s3.headObject(params).promise()
        console.log("res is ",res)
        return true
    } catch(error){
        console.log("error is ",error)
        return false
    }
}

router.get('/download/url/open', function(request, response,next){
  const download_file_path = request.query.file_name
    async function get_url(){
        try{
            if(!download_file_path){
                throw new Error("Empty download file path")
            }
            var download_file_params = {
                Bucket: process.env.S3_PUBLIC_FILES, 
                Key: download_file_path
            };

            const exists = await check_download_exists(download_file_params)
            if(exists){
                const url = s3.getSignedUrl('getObject', {
                    Bucket: process.env.S3_PUBLIC_FILES,
                    Key: download_file_path,
                    Expires: 30
                })
                response.status(200).send(url)
                // insert into pg table for audit
            }
            else{
                next(new Error("No downloads available"))
            }
        }catch(error){
            next(new Error("URL generation failed"))
        }
    }
    get_url()

})


router.get('/download/url/controlled', function(request, response,next){
    const b_token = request.headers['authorization']; 
    const token = b_token.replace(/^Bearer\s+/, "");
    console.log("token is: ",token)
    // check if bearer token is present, if yes then parse token for validity
    if(token){
        jwt.verify(token,process.env.SIGN_KEY,{algorithms: "HS256"}, function(err,decoded){
            if(err){
                console.log("errr is ",err)
                next(new Error("Token verification failed"))
                return
            } 
            // decrypt to get db_name  -> if all good,  send directly pre-signed URL
            if(decoded){
                console.log("decoded is ",decoded)
                const download_file_path = request.query.file_name
                const key = process.env.ENC_KEY;
                const iv= process.env.ENC_IV;
                var decipher = crypto.createDecipheriv('aes-256-cbc',key,iv)
                var de_token=decipher.update(decoded["payload"],'hex','utf-8');
                de_token+=decipher.final();
                console.log("de token is",de_token)
                const dataset_name=JSON.parse(de_token)["dataset"]
                console.log("dataset name is ",dataset_name)
                // generate pre-signed url and return
                async function get_url(){
                    try{
                        if(!download_file_path){
                            throw new Error("Empty download file path")
                        }
                        var download_file_params = {
                            Bucket: process.env.S3_DATASET_PREFIX+"-"+dataset_name+"-controlled", 
                            Key: download_file_path
                        };
                        console.log("params are: ",download_file_params)

                        const exists = await check_download_exists(download_file_params)
                        if(exists){
                            const url = s3.getSignedUrl('getObject', {
                                Bucket: process.env.S3_DATASET_PREFIX+"-"+dataset_name+"-controlled",
                                Key: download_file_path,
                                Expires: 30
                            })
                            response.status(200).send(url)
                            // insert into pg table for audit
                            const requested_time=new Date();
                            const file_audit_fn=async function(){
                                const client = await pool.connect()
                                try{
                                    const file_audit_text='INSERT INTO public.controlled_file_audits( \
                                        dataset_slug, bearer_token, requested_file_path, requested_at) \
                                        VALUES ( $1, $2, $3,$4);'
                                    client.query(file_audit_text, [dataset_name,token,download_file_path,requested_time],function(err,res){
                                        if (err){
                                            console.log("err is ",err)
                                            console.log("System Error in inserting into file audit table")
                                        }
                                    })
                                } catch(error){
                                    console.log("Error in inserting into file audit table")
                                } finally{
                                    client.release();
                                }
                            }
                            file_audit_fn();
                        }
                        else{
                            next(new Error("No downloads available"))
                        }
                    }catch(error){
                        next(new Error("URL generation failed"))
                    }
                }
                get_url()

            }
        })
    } else{
        next(new Error("Invalid request"))
    }
});

router.get('/health', function(request, response, next) {
    const healthcheck_resp = {
		message: 'OK',
		timestamp: Date.now()
	};
    response.status(200).send(healthcheck_resp);
  });

app.use('/api/v1',router);

app.use(function (err, req, res, next) {
    res.status(err.status || 500).send(err.message)
});
