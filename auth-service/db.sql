--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7
-- Dumped by pg_dump version 14.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: authn_authz; Type: TABLE; Schema: public; Owner: xxxxxxxx
--

CREATE TABLE public.authn_authz (
    user_id bigint NOT NULL,
    email character varying NOT NULL,
    authentication_token character varying NOT NULL,
    dataset_id bigint NOT NULL,
    dataset_slug character varying NOT NULL
);


ALTER TABLE public.authn_authz OWNER TO xxxxxxxx;

--
-- Name: bearer_token_audit; Type: TABLE; Schema: public; Owner: xxxxxxxx
--

CREATE TABLE public.bearer_token_audit (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    user_token character varying NOT NULL,
    requested_dataset_slug character varying NOT NULL,
    final_requested_dataset_slug character varying NOT NULL,
    bearer_token character varying NOT NULL,
    requestor_ip character varying NOT NULL,
    created_at character varying NOT NULL
);


ALTER TABLE public.bearer_token_audit OWNER TO xxxxxxxx;

--
-- Name: bearer_token_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: xxxxxxxx
--

ALTER TABLE public.bearer_token_audit ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.bearer_token_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000000
    CACHE 1
);


--
-- Name: controlled_file_audits; Type: TABLE; Schema: public; Owner: xxxxxxxx
--

CREATE TABLE public.controlled_file_audits (
    id bigint NOT NULL,
    dataset_slug character varying NOT NULL,
    bearer_token character varying NOT NULL,
    requested_file_path character varying NOT NULL,
    requested_at timestamp without time zone NOT NULL
);


ALTER TABLE public.controlled_file_audits OWNER TO xxxxxxxx;

--
-- Name: dataset_file_audits_id_seq; Type: SEQUENCE; Schema: public; Owner: xxxxxxxx
--

ALTER TABLE public.controlled_file_audits ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dataset_file_audits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000000000
    CACHE 1
);

--
-- Name: invalid_auth; Type: TABLE; Schema: public; Owner: postgres_nsrr
--

CREATE TABLE public.invalid_auth (
    id bigint NOT NULL,
    ip character varying,
    token character varying,
    user_agent character varying
);


ALTER TABLE public.invalid_auth OWNER TO xxxxxxxx;

--
-- Name: invalid_auth_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres_nsrr
--

ALTER TABLE public.invalid_auth ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.invalid_auth_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000000
    CACHE 1
);


--
-- Name: bearer_token_audit bearer_token_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: xxxxxxxx
--

ALTER TABLE ONLY public.bearer_token_audit
    ADD CONSTRAINT bearer_token_audit_pkey PRIMARY KEY (id);


--
-- Name: controlled_file_audits dataset_file_audits_pkey; Type: CONSTRAINT; Schema: public; Owner: xxxxxxxx
--

ALTER TABLE ONLY public.controlled_file_audits
    ADD CONSTRAINT dataset_file_audits_pkey PRIMARY KEY (id);


--
-- Name: invalid_auth invalid_auth_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres_nsrr
--

ALTER TABLE ONLY public.invalid_auth
    ADD CONSTRAINT invalid_auth_pkey PRIMARY KEY (id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: xxxxxxxx
--

REVOKE ALL ON SCHEMA public FROM xxxxxxxx;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO xxxxxxxx;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

