const AWS = require('aws-sdk');
const fs = require('fs')

if(process.argv.length !=3){
    console.log("Expecting only 1 input parameter. Run command is node get_s3_files_list.js <dataset_name>")
    return
}
var dataset_name= process.argv[2]

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

async function get_files(params){
    var all_files = []
    const res = await s3.listObjectsV2(params).promise();
    res.Contents.forEach(file_obj => all_files.push(file_obj));
    if (res.NextContinuationToken) {
      params.ContinuationToken = res.NextContinuationToken;
      await get_files(params); 
    }
    return all_files;
}

function get_files_list(dataset_name, control_type){
    const all_files=async function() {
        try{
            if(!datasets_list.includes(dataset_name)){
                throw new Error(dataset_not_found_error)
            }
            let open_files={}
            const open_files_list = await get_files({ Bucket: process.env.S3_PUBLIC_FILES,Prefix: dataset_name+'/' });
            for(let i=0;i<open_files_list.length; i++){
                if(open_files_list[i]["Size"]!=0){
                    open_files[open_files_list[i]["Key"]]={
                        "md5":open_files_list[i]["ETag"].replace(/\"/g,''),
                        "size": open_files_list[i]["Size"]
                    }
                }
            }
            let controlled_files={}
            if(control_type == "controlled"){
                const controlled_files_list = await get_files({ Bucket: process.env.S3_DATASET_PREFIX+"-"+dataset_name+"-controlled"});
                for(let i=0;i<controlled_files_list.length; i++){
                    if(controlled_files_list[i]["Size"]!=0){
                        controlled_files[controlled_files_list[i]["Key"]]={
                            "md5":controlled_files_list[i]["ETag"].replace(/\"/g,''),
                            "size": controlled_files_list[i]["Size"]
                        }
                    }     
                }

            }

            let final_json={}
            final_json['open_files']=open_files
            final_json['controlled_files']=controlled_files

            fs.writeFile("metadata/"+dataset_name+'_metadata.json', JSON.stringify(final_json), 'utf8', function(err){
                if(err){
                    throw(err)
                }
                console.log("completed")
            });
        } catch(error){
            console.log(error)
        }
    }
    all_files();

}

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
    var control_type="controlled"
    metadata_list.forEach(set => {
        if(set.split(",")[0] == dataset_name){
            if(set.split(",")[1] == "open"){
                control_type="open"
            }
        }
    });
    get_files_list(dataset_name, control_type)
  })


