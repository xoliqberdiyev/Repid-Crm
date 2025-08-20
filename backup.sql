--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

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

--
-- Name: expensefromwhom; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.expensefromwhom AS ENUM (
    'oybek',
    'bahrom',
    'income'
);


ALTER TYPE public.expensefromwhom OWNER TO postgres;

--
-- Name: expensetype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.expensetype AS ENUM (
    'employee_salary',
    'for_office',
    'smm_service',
    'renting',
    'other_expense',
    'office_item',
    'tax'
);


ALTER TYPE public.expensetype OWNER TO postgres;

--
-- Name: incometype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.incometype AS ENUM (
    'from_student',
    'from_project',
    'investor'
);


ALTER TYPE public.incometype OWNER TO postgres;

--
-- Name: statusexpectedvalue; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.statusexpectedvalue AS ENUM (
    'income',
    'expense'
);


ALTER TYPE public.statusexpectedvalue OWNER TO postgres;

--
-- Name: statusoperator; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.statusoperator AS ENUM (
    'in_progres',
    'done',
    'cancel',
    'empty',
    'repeat'
);


ALTER TYPE public.statusoperator OWNER TO postgres;

--
-- Name: statusproject; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.statusproject AS ENUM (
    'in_progres',
    'done',
    'cancel'
);


ALTER TYPE public.statusproject OWNER TO postgres;

--
-- Name: statustask; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.statustask AS ENUM (
    'to_do',
    'in_progres',
    'done',
    'success',
    'code_review'
);


ALTER TYPE public.statustask OWNER TO postgres;

--
-- Name: usertype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.usertype AS ENUM (
    'super_admin',
    'admin',
    'custom'
);


ALTER TYPE public.usertype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: chat_room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_room (
    id integer NOT NULL,
    user1_id integer NOT NULL,
    user2_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.chat_room OWNER TO postgres;

--
-- Name: chat_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chat_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_room_id_seq OWNER TO postgres;

--
-- Name: chat_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chat_room_id_seq OWNED BY public.chat_room.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    first_name character varying(100),
    username character varying(100) NOT NULL,
    last_name character varying(100),
    phone_number character varying(50),
    date_of_birth timestamp without time zone,
    date_of_jobstarted timestamp without time zone,
    position_id integer,
    image character varying,
    salary bigint,
    user_type public.usertype NOT NULL,
    password character varying NOT NULL,
    is_active boolean NOT NULL,
    created_time timestamp without time zone NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: expected_value; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.expected_value (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    date timestamp without time zone,
    description character varying NOT NULL,
    type public.statusexpectedvalue NOT NULL,
    price bigint NOT NULL
);


ALTER TABLE public.expected_value OWNER TO postgres;

--
-- Name: expected_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.expected_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.expected_value_id_seq OWNER TO postgres;

--
-- Name: expected_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.expected_value_id_seq OWNED BY public.expected_value.id;


--
-- Name: expences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.expences (
    id integer NOT NULL,
    name character varying,
    real_price character varying,
    price_paid character varying(100) NOT NULL,
    description character varying,
    date_paied timestamp without time zone NOT NULL,
    employee_salary_id integer,
    type public.expensetype NOT NULL,
    from_whom public.expensefromwhom
);


ALTER TABLE public.expences OWNER TO postgres;

--
-- Name: expences_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.expences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.expences_id_seq OWNER TO postgres;

--
-- Name: expences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.expences_id_seq OWNED BY public.expences.id;


--
-- Name: incomes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.incomes (
    id integer NOT NULL,
    name character varying(100),
    real_price character varying(100),
    pay_price character varying(100),
    date_paied timestamp without time zone,
    "position" character varying,
    project_id integer,
    type public.incometype NOT NULL,
    description character varying
);


ALTER TABLE public.incomes OWNER TO postgres;

--
-- Name: incomes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.incomes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.incomes_id_seq OWNER TO postgres;

--
-- Name: incomes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.incomes_id_seq OWNED BY public.incomes.id;


--
-- Name: login_pass_note; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.login_pass_note (
    id integer NOT NULL,
    login character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.login_pass_note OWNER TO postgres;

--
-- Name: login_pass_note_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.login_pass_note_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.login_pass_note_id_seq OWNER TO postgres;

--
-- Name: login_pass_note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.login_pass_note_id_seq OWNED BY public.login_pass_note.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message (
    id integer NOT NULL,
    chat_id integer NOT NULL,
    sender_id integer NOT NULL,
    content character varying(200) NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.message OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.message_id_seq OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_seq OWNED BY public.message.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer,
    message character varying(300) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_read boolean NOT NULL
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: operator_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operator_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.operator_type OWNER TO postgres;

--
-- Name: operator_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operator_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.operator_type_id_seq OWNER TO postgres;

--
-- Name: operator_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operator_type_id_seq OWNED BY public.operator_type.id;


--
-- Name: operators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operators (
    id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    phone_number character varying(100) NOT NULL,
    description character varying NOT NULL,
    status public.statusoperator NOT NULL,
    operator_type_id integer NOT NULL
);


ALTER TABLE public.operators OWNER TO postgres;

--
-- Name: operators_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.operators_id_seq OWNER TO postgres;

--
-- Name: operators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operators_id_seq OWNED BY public.operators.id;


--
-- Name: positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.positions (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.positions OWNER TO postgres;

--
-- Name: positions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.positions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.positions_id_seq OWNER TO postgres;

--
-- Name: positions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.positions_id_seq OWNED BY public.positions.id;


--
-- Name: project_programmer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_programmer (
    id integer NOT NULL,
    project_id integer NOT NULL,
    programmer_id integer NOT NULL
);


ALTER TABLE public.project_programmer OWNER TO postgres;

--
-- Name: project_programmer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_programmer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_programmer_id_seq OWNER TO postgres;

--
-- Name: project_programmer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_programmer_id_seq OWNED BY public.project_programmer.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    status public.statusproject NOT NULL,
    image character varying NOT NULL,
    price character varying,
    is_deleted boolean
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_id_seq OWNER TO postgres;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: task_programmer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_programmer (
    id integer NOT NULL,
    task_id integer NOT NULL,
    programmer_id integer NOT NULL
);


ALTER TABLE public.task_programmer OWNER TO postgres;

--
-- Name: task_programmer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_programmer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_programmer_id_seq OWNER TO postgres;

--
-- Name: task_programmer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_programmer_id_seq OWNED BY public.task_programmer.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    status public.statustask NOT NULL,
    is_deleted boolean,
    description character varying NOT NULL,
    image_task character varying(100)
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: chat_room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_room ALTER COLUMN id SET DEFAULT nextval('public.chat_room_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: expected_value id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expected_value ALTER COLUMN id SET DEFAULT nextval('public.expected_value_id_seq'::regclass);


--
-- Name: expences id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expences ALTER COLUMN id SET DEFAULT nextval('public.expences_id_seq'::regclass);


--
-- Name: incomes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incomes ALTER COLUMN id SET DEFAULT nextval('public.incomes_id_seq'::regclass);


--
-- Name: login_pass_note id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login_pass_note ALTER COLUMN id SET DEFAULT nextval('public.login_pass_note_id_seq'::regclass);


--
-- Name: message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: operator_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operator_type ALTER COLUMN id SET DEFAULT nextval('public.operator_type_id_seq'::regclass);


--
-- Name: operators id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operators ALTER COLUMN id SET DEFAULT nextval('public.operators_id_seq'::regclass);


--
-- Name: positions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions ALTER COLUMN id SET DEFAULT nextval('public.positions_id_seq'::regclass);


--
-- Name: project_programmer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_programmer ALTER COLUMN id SET DEFAULT nextval('public.project_programmer_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: task_programmer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_programmer ALTER COLUMN id SET DEFAULT nextval('public.task_programmer_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
b913c86b0a7a
\.


--
-- Data for Name: chat_room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_room (id, user1_id, user2_id, created_at) FROM stdin;
1	6	4	2025-04-10 13:54:27.909109
2	7	6	2025-04-10 15:11:29.157781
3	8	6	2025-04-10 15:13:34.664275
4	3	6	2025-04-11 13:58:50.134743
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, first_name, username, last_name, phone_number, date_of_birth, date_of_jobstarted, position_id, image, salary, user_type, password, is_active, created_time) FROM stdin;
12	Afzal	Pulatov	Pulatov	+998909103262	\N	2024-10-23 00:00:00	6	\N	3000000	custom	$2b$12$vejEIdJsDDZaFE713XqOreZgIOtR1nlCgvSzM8s6/jC8CNbgGGgn.	t	2025-02-05 16:33:09.108698
28	Yusufbek	Yusufbek	Khamidullaev	+998949207161	2008-04-14 00:00:00	2025-04-20 00:00:00	3	\N	500000	custom	$2b$12$XxLCq5T4ZzY9Z9t2dEn1iOKEyoKIUSIjsfRlvp41koyemQgNIM.S6	t	2025-04-11 14:00:30.89807
13	Anvar	Anvar_6268	Maqsudov	+998909106268	\N	2024-11-11 00:00:00	6	\N	100000	custom	$2b$12$CGXlFrpKO.u0lSGBnLHTGOT2rD5MRZXZmUT1yIweLHsGvkkGCE9TO	t	2025-02-08 12:06:43.945902
15	Bobadiyor	Bobadiyor	Bugalter	+998200002249	2025-02-05 00:00:00	2024-10-23 00:00:00	2	\N	450000	custom	$2b$12$bspNPj9p9zu0Zm0JY9Zjcuq1dcS0epCVGVVSlsI7CXXVKp/BV04wG	t	2025-02-08 12:06:43.945902
16	Oybek	Oybek_0487	Olimovich	+998977700487	2025-02-22 00:00:00	2024-10-15 00:00:00	7	\N	0	custom	$2b$12$LFweeNB2U95fibgu/zde/.Gb95MpE7F082E0pvJyegmz8Ji3YGfIO	t	2025-02-08 12:06:43.945902
17	Bahrom	Bahrom_5599	Tohirov	+99894	2025-02-15 00:00:00	2024-10-15 00:00:00	7	\N	0	custom	$2b$12$wNOsbk6B4unjP/sIGVodMO9aVTP.U1UfqP0Wo9nmxf0Sahzh3HqPe	t	2025-02-08 12:06:43.945902
20	Maftuna	Maftuna	Tursunova	+998977777777	2024-12-05 00:00:00	2024-11-04 00:00:00	2	\N	1000000	custom	$2b$12$sWSBwjgH4ilG0M6CYgy91.FRsh5kYHl/s04zMW8uxuFPA3HRyV9xu	t	2025-02-08 12:06:43.945902
2	Oybek	oybek	Tojiyev	+998977700487	\N	2024-10-05 00:00:00	1	\N	0	super_admin	$2b$12$F6g7s/7sKJLDWnRIaeSdpeVg4ks5j5RCnYs7eqNJ5RYET/BPGh6uK	t	2025-02-05 14:17:25.918262
14	Farrosh ayol	Farrosh ayol	ayol	+99897777777	\N	2024-10-23 00:00:00	8	\N	200000	custom	$2b$12$A3SYaWRTGYIkKxv5YTRl.e7be0wNQhlqLBVlOo9q2ejea8YGJ0yoG	t	2025-02-08 12:06:43.945902
3	Behruz	real_man	Xoliqberdiyev	+998947099971	2009-09-12 00:00:00	2024-11-01 00:00:00	2	profile.jpg	1000000	custom	$2b$12$kNsDvsNUZskdpYiAbo13OeQS6Mz61RmJqu.wdDF.whhnrsTs9uOXu	t	2025-02-05 14:17:25.918262
22	Mavlon	------	Zokirov	+998904490929	\N	2025-03-03 00:00:00	3	\N	1000000	custom	$2b$12$FgPQaXDUj7Y92TM1sXuBluxVxjIjxllVcO/frayPxzyr22D15b2IG	t	2025-02-28 14:31:11.543623
8	Jahongir	ismoil	Husanov	+998977042553	2008-08-04 00:00:00	2025-01-27 00:00:00	3	images.jpg	1000000	custom	$2b$12$8AG/NBDyaBo.I/w2r2FTue4T6sy28mHndgnUEdoMygNxkRZ1O44Ii	t	2025-02-05 14:17:25.918262
11	Diyorbek	Diyorbek	Ibrohimov	+998935037720	2004-04-05 00:00:00	2024-10-18 00:00:00	7	\N	1500000	admin	$2b$12$iuRFju6nxfEahwTkcTtNi.XqrsiquszzUv/NmgCxR6nuavGkOoLMS	t	2025-02-05 16:33:09.108698
19	Sardor	Sardor	SMM	+998947700487	2025-02-01 00:00:00	2024-11-12 00:00:00	5	\N	1000000	custom	$2b$12$osl0AiFK2W24j2zUWRLtW.ey2MuzhULkL7UT1qe2Nl./ChZtMvOB6	t	2025-02-08 12:06:43.945902
18	Shahzod	Shahzod_6263	Burxonov	+998906756263	2025-02-01 00:00:00	2024-10-21 00:00:00	4	\N	1500000	super_admin	$2b$12$IKpmT9C.igkDB4LxzhUGYeRcW0VGDuduskJ5JCrNM.agPDX.EH7ju	t	2025-02-08 12:06:43.945902
4	Shahzod	shahzod_king	Abdashev	+998949252945	2005-07-09 00:00:00	2024-11-01 00:00:00	2	my_picture.jpg	1000000	super_admin	$2b$12$1bEsQ4CQJMhiXl8YJy/pw.bXWlFC7DOYByZrPx8pcyGS1QZ8MFDJO	t	2025-02-05 14:17:25.918262
31	Bahtiyor	bahtiyor	Hamidullayev	+998995164433	2025-08-05 00:00:00	2025-08-06 00:00:00	3	\N	1000000	custom	$2b$12$b.9t1rrmTI8xHF6iphTeCOLDk8TpCkgFIIOEeltuZkFFryT07JzWm	t	2025-07-26 10:57:49.255247
5	Nodirbek	nodir_zafarovich	Soliyev	+998947853060	2005-12-06 00:00:00	2025-01-01 00:00:00	3	\N	1000000	custom	$2b$12$znOzxWnnkiF3jD.u2fNAuORwgmchcsFqOu6FervEnLz07k/iS1yia	f	2025-02-05 14:17:25.918262
7	Mavlon	mavlon_turgunof	Turgunov	+998950420319	2002-03-19 00:00:00	2024-10-16 00:00:00	3	\N	1000000	custom	$2b$12$lnoe8ggGlsNIQLl9GmcP1eEu.g8JRqzBcXM8Q/4bhafQl1nPHQfGe	t	2025-02-05 14:17:25.918262
29	Shahzod 	shahzod	Abdashev	+998949252945	2025-04-30 00:00:00	2024-11-01 00:00:00	2	\N	1000000	custom	$2b$12$Zs4LwuRpjz.cXq1/j2Sswe.iNxjjBntgnwgXp1dxOZGSWYkWnJeYC	t	2025-04-29 16:12:39.208359
32	\N	Repid001_	\N	\N	\N	\N	\N	\N	\N	super_admin	Repid001_	t	2025-08-13 14:10:03.805043
33	Admin	admin	User	+998901234567	\N	\N	\N	\N	\N	super_admin	$2b$12$AbCdEfGhIjKlMnOpQrStUvWxYz	t	2025-08-16 07:31:13.743618
9	Xudoyorxon	ad1988491	Avazxonov	+998882062100	2006-01-21 00:00:00	2025-01-18 00:00:00	6	\N	1000000	custom	$2b$12$JlQPXPvgashVLoNgISjmPOEpLLDd3DcQsaoxu5d8fTJiijg2WTyYG	t	2025-02-05 14:17:25.918262
6	Nodir	jahongir000	Soliyev	+998904490924	\N	2024-10-26 00:00:00	3	\N	1000000	custom	$2b$12$uUQ5tmVT07dqqXGAvSpz4.HOVIk2EUiutuKVp75uqr8lVzenIRam2	t	2025-02-05 14:17:25.918262
30	Abdurauf	Abdurauf	Ramiz	+998930029571	2009-06-27 00:00:00	2025-07-06 00:00:00	3	\N	1000000	custom	$2b$12$bHgsz5g/8EBFPsjBE/Infe.Nncjhz2U3zUJ3.41bBwZpOE00p2W76	t	2025-07-02 18:02:25.381261
\.


--
-- Data for Name: expected_value; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.expected_value (id, name, date, description, type, price) FROM stdin;
1	Arenda	2025-02-10 00:00:00	Fevral oyi uchun arenda puli	expense	7800000
2	Shahzod Flatter	2025-02-28 00:00:00	Oyligidan qarzimiz	expense	200000
3	Bugalter	2025-02-15 00:00:00	Fevral oyi oyligi	expense	650000
5	Afzal Dizayner Oylik	2025-02-23 00:00:00	Oylik	expense	3000000
9	Telegiram kanal reklamasi	2025-02-15 00:00:00	Telegiram orqali mijoz topish uchun\n	expense	1300000
11	Sardor Smm oylik	2025-02-10 00:00:00	Sarodr oyligi	expense	1000000
12	Derektor xonasiga jaluzi	2025-02-28 00:00:00	Derektor honasiga oftob tushmasligi uchun	expense	1300000
13	Suv uchun kuller	2025-02-28 00:00:00	Suvni kullerda issiq muzdek qilib ichish uchun	expense	1300000
14	Doska	2025-02-28 00:00:00	Ishni sifatini oshirish uchun	expense	500000
15	Tilvizor	2025-02-28 00:00:00	Confort yaratish uchun 	expense	3000000
16	Diyorbek komponiyasi qarzi	2025-02-28 00:00:00	Diyordan nayabr oyida afzalni oyligini berish uchun olingan qarz	expense	1700000
17	Afzaldan qarz 	2025-02-28 00:00:00	Afzaldan nayabr oyida smm yurgazgani uchun olingan qarz	expense	1000000
18	Kitoblar	2025-02-28 00:00:00	Ofisda ilim olish va kutubxona yaratish uchun	expense	650000
19	Motostan puli 	2025-02-15 00:00:00	Motostan prayektini topshirib pulini olish kerak	income	1300000
20	Motostan support	2025-02-15 00:00:00	Oylik Support puli	income	2600000
21	OnePc praykt puli	2025-02-15 00:00:00	OnePc prayektni topshirish kerak	income	2400000
22	One PC support 	2025-02-15 00:00:00	Oylik supportni undirish kerak	income	2600000
23	Moy zavod	2025-02-15 00:00:00	Prayektni ohirgi yarim puli	income	7800000
\.


--
-- Data for Name: expences; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.expences (id, name, real_price, price_paid, description, date_paied, employee_salary_id, type, from_whom) FROM stdin;
85	Izalenta	\N	5000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
82	Stul boltlari	\N	35000	Bahrom	2024-11-03 00:00:00	\N	for_office	bahrom
83	2 ta ruchka	\N	4000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
88	Gel	\N	5000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
41	Broker	\N	650000	Kirimdan	2025-01-27 00:00:00	\N	other_expense	income
13	Kechki ovqat	\N	90000	Bahrom	2024-10-15 00:00:00	\N	other_expense	bahrom
27	10 L suv	\N	14000		2025-02-04 00:00:00	\N	for_office	oybek
237	Server harajatlari	\N	120000	Kirimdan	2025-03-12 00:00:00	\N	for_office	income
239	Vedio Studio arenda	\N	250000		2025-03-12 00:00:00	\N	smm_service	income
17	Yuk mashina	\N	48000	Kirimdan\n	2024-10-28 00:00:00	\N	other_expense	income
221	Arenda	\N	1500000	Kirimdan	2025-02-13 00:00:00	\N	renting	income
249	\N	\N	1000000	\N	2025-03-19 00:00:00	3	employee_salary	\N
48	Restaran aylangani chiqqanda ovqatlanishga	\N	32000	kirimdan	2024-11-04 00:00:00	\N	other_expense	income
223	\N	\N	200000	\N	2025-02-22 00:00:00	14	employee_salary	\N
12	Yuk mashina	\N	150000	Bahrom	2024-10-15 00:00:00	\N	other_expense	bahrom
253	\N	\N	500000	\N	2025-02-10 00:00:00	19	employee_salary	\N
202	\N	\N	2190000	\N	2024-11-30 00:00:00	16	employee_salary	\N
203	\N	\N	350000	\N	2025-01-31 00:00:00	16	employee_salary	\N
78	Yandex gruzga	\N	150000	Bahrom	2025-01-15 00:00:00	\N	other_expense	income
1	Telefon Raqam olish	\N	35000	Kirimdan	2024-10-10 00:00:00	\N	for_office	income
4	Yagona daracha to'lov	\N	500000	Bahrom	2024-10-15 00:00:00	\N	tax	bahrom
3	Yagona darcha to'lov	\N	450000	Oybek	2024-10-15 00:00:00	\N	tax	oybek
37	App Store Yillik summa	\N	1300000	Kirimdan	2025-01-27 00:00:00	\N	office_item	income
2	Tilifon Oylik tarif	\N	50000	Kirimdan	2024-10-10 00:00:00	\N	for_office	income
11	\N	\N	1000000	\N	2025-01-31 00:00:00	5	employee_salary	\N
224	Aylanma soliq	\N	1252000	Yanvar oyi uchun soliq	2025-02-25 00:00:00	\N	tax	income
230	\N	\N	450000	\N	2025-02-25 00:00:00	15	employee_salary	\N
45	Boshqa kichik Soliqlar uchun	\N	7000	Kirimdan	2025-01-24 00:00:00	\N	tax	income
57	Daromaddan soliq ( Oylikdan soliq olingan )	\N	288000	Kirimdan	2025-01-24 00:00:00	\N	tax	income
56	Diverent Solig'i	\N	1350000	Kirimdan	2025-01-24 00:00:00	\N	tax	income
84	Schovoch	\N	15000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
98	Qahva Nescafe Gold	\N	100000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
79	Nalog kluchka	\N	37500	Bahrom	2024-10-24 00:00:00	\N	tax	bahrom
100	Restaran aylangani chiqqanda avtobusga	\N	8000	Kirimdan	2023-11-04 00:00:00	\N	other_expense	income
231	Arenda naqt	\N	2000000	Kirimdan	2025-02-26 00:00:00	\N	renting	income
15	Ofisga suv	\N	38000	Bahrom	2024-10-24 00:00:00	\N	for_office	income
96	Quruq choy 	\N	20000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
94	Limanat Barbicon	\N	16000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
95	Vilajniy salfetka	\N	12000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
233	One Pc ga borishga	\N	50000	One Pc ga borishga taxtiga bollarga berdim Mavlon Shahzodga	2025-03-05 00:00:00	\N	other_expense	income
20	2 ruchka	\N	4000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
21	Skoch	\N	15000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
97	Qant	\N	15000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
93	Barjome suv	\N	14000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
90	Bumaga	\N	10000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
14	fleshka	\N	45000	Bahrom	2024-10-24 00:00:00	\N	for_office	bahrom
273	\N	\N	123456	\N	2025-03-22 00:00:00	\N	employee_salary	\N
279	Arenda naqt	\N	6100000	3 marta bo'lib bo'lib pul to'ladim \n	2025-04-02 00:00:00	\N	renting	income
281	We-fi to'lovi	\N	350000	300 ming we-fi oylik to'lovi 50 ming ustanivka	2025-04-04 00:00:00	\N	for_office	income
28	10 L suv	\N	14000	Kirimdan 	2025-01-31 00:00:00	\N	for_office	income
288	10 L suv	\N	12000		2025-04-22 00:00:00	\N	for_office	income
289	Bank foiz,plastik foiz	\N	80000	$ maydalaganimdagi yo'qotish, plastikdan foiz	2025-04-29 00:00:00	\N	other_expense	income
296	Server 1 uchun	\N	220000	Serverga oylik to'lov	2025-04-29 00:00:00	\N	for_office	income
297	Server 2 uchun	\N	220000	Server 2 oylik to'lov uchun	2025-04-30 00:00:00	\N	for_office	income
32	10 L suv	\N	13000	Kirimdan	2025-01-28 00:00:00	\N	for_office	income
298	\N	\N	500000	\N	2025-04-30 00:00:00	6	employee_salary	\N
59	Bumaga	\N	16000	Kirimdan	2025-01-25 00:00:00	\N	for_office	income
61	2 ta 10 L suv	\N	26000	Kirimdan	2025-01-25 00:00:00	\N	for_office	income
60	Konfet 500 gram	\N	40000	Kirimdan	2025-01-25 00:00:00	\N	for_office	income
62	Server To'lovi	\N	110000	Kirimdan	2025-01-13 00:00:00	\N	for_office	income
63	Telefon Oylik to'lovi	\N	50000	Kirimdan	2025-01-07 00:00:00	\N	for_office	income
65	Kalit yasattirishga 	\N	25000	Kirimdan	2024-12-26 00:00:00	\N	for_office	income
76	120 L suv	\N	75000	Bahrom	2024-12-17 00:00:00	\N	for_office	income
75	Qog'oz sochiq	\N	20000	Kirimdan	2024-12-17 00:00:00	\N	for_office	income
74	Bumaga	\N	15000	Kirimdan	2024-12-17 00:00:00	\N	for_office	income
69	10L Suvga	\N	12000	Kirimdan	2024-11-11 00:00:00	\N	for_office	income
67	Musur paket	\N	10000	Kirimdan	2024-11-06 00:00:00	\N	for_office	income
66	Telefonga paynet	\N	50000	Kirimdan	2024-11-06 00:00:00	\N	for_office	income
101	Qog'oz sochiq uchun	\N	12000	Kirimdan	2024-11-05 00:00:00	\N	for_office	income
22	Izalante	\N	5000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
19	Stul boltlari	\N	35000	Bahrom	2024-11-04 00:00:00	\N	for_office	income
24	Gel	\N	5000	Kirimdan\n	2024-11-04 00:00:00	\N	for_office	income
25	Aloe vera suv	\N	10000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
30	BimBom kanfet	\N	33000	Kirimdan\n	2024-11-04 00:00:00	\N	for_office	income
46	Qant 	\N	15000	kirimdan	2024-11-04 00:00:00	\N	for_office	income
47	Qahva Nescafe Gold	\N	100000	kirimdan	2024-11-04 00:00:00	\N	for_office	income
39	Quruq choy	\N	20000	kirimdan\n	2024-11-04 00:00:00	\N	for_office	income
51	Qog'oz sochiq uchun	\N	12000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
89	Aloe vera suv	\N	10000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
8	\N	\N	1000000	\N	2025-01-31 00:00:00	4	employee_salary	\N
9	\N	\N	1000000	\N	2025-01-31 00:00:00	7	employee_salary	\N
10	\N	\N	1000000	\N	2025-01-31 00:00:00	6	employee_salary	\N
35	Video Studio	\N	300000	Kirimdan	2025-01-27 00:00:00	\N	smm_service	income
64	Video Studio	\N	205000	Kirimdan	2024-11-06 00:00:00	\N	smm_service	income
305	Arenda aprel	\N	3000000		2025-04-30 00:00:00	\N	renting	income
315	10 L suv	\N	14000		2025-05-19 00:00:00	\N	for_office	income
317	\N	\N	200000	\N	2025-05-22 00:00:00	14	employee_salary	\N
323	Pensiya badali uchun ajratma	\N	3000	Iyun oyida to'ladim	2025-05-15 00:00:00	\N	tax	income
110	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	20000	Kirimdan	2024-11-19 00:00:00	\N	other_expense	income
132	100 L suv	\N	100000	Kirimdan	2024-11-18 00:00:00	\N	for_office	income
120	Qora choy	\N	7000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
102	10 L suv	\N	12000	Kirimdan	2024-11-05 00:00:00	\N	for_office	income
204	Kitob 	\N	125000	Kirimdan	2025-01-27 00:00:00	\N	office_item	income
205	Aylanma Mabilag'dan soliq	\N	1566000	Kirimdan	2025-01-24 00:00:00	\N	tax	income
207	1 ta Stol  6 ta Stul	\N	1470000	Kirimdan	2024-10-28 00:00:00	\N	office_item	income
225	Ijtimoiy soliq	\N	360000	Yanvar oyi soliq	2025-02-25 00:00:00	\N	tax	income
232	Komputer	\N	100000	Someting	2024-01-01 00:00:00	\N	for_office	oybek
235	120 L suv	\N	90000		2025-03-05 00:00:00	\N	for_office	income
258	Soliqlar	\N	900000	Fevral oyi soliqlari	2025-03-20 00:00:00	\N	tax	income
222	Diyorni o'qishi uchun 	\N	1300000	Oybek.	2025-02-08 00:00:00	\N	office_item	oybek
256	\N	\N	450001	\N	2025-03-20 00:00:00	\N	employee_salary	\N
248	\N	\N	1000001	\N	2025-03-19 00:00:00	\N	employee_salary	\N
274	\N	\N	123456	\N	2025-03-22 00:00:00	\N	employee_salary	\N
280	Server to'lovi	\N	210000	2 oylik qarzdorlik yopildi	2025-04-03 00:00:00	\N	for_office	income
290	Arendaga naqt	\N	6100000	Aprel oy uchun 	2025-04-29 00:00:00	\N	renting	income
299	Mikrafon uzum nasiyadan	\N	2348000	Smm vediolar uchun mikrafon uzum nasiyadan olganimiz uchun qimmat bo'ldi	2025-04-29 00:00:00	\N	office_item	income
306	20 L suv	\N	26000		2025-05-08 00:00:00	\N	for_office	income
310	Confort syomkaga borganda harajat	\N	100000	Obet yo'l kira moshinaga benzin	2025-05-12 00:00:00	\N	other_expense	income
316	10 L suv	\N	14000		2025-05-22 00:00:00	\N	for_office	income
318	Jismoniy shahslardan daromad solig'i	\N	278000	Soliq iyun oyida to'ladim	2025-04-12 00:00:00	\N	tax	income
322	Ijtimoiy soliq	\N	364000	Iyun oyi to'ladim	2025-05-15 00:00:00	\N	tax	income
325	Server 2 to'lovi	\N	200000		2025-06-04 00:00:00	\N	for_office	income
330	Mobilogivga mantaj uchun	\N	650000	3 ta vedioni mantaj qilib bergani uchun	2025-06-01 00:00:00	\N	smm_service	income
331	Arenda may oyi	\N	9100000		2025-05-31 00:00:00	\N	renting	income
338	\N	\N	3000000	\N	2025-05-23 00:00:00	12	employee_salary	\N
352	We fi to'lovi	\N	330000		2025-07-01 00:00:00	\N	for_office	income
357	\N	\N	1000000	\N	2025-04-04 00:00:00	22	employee_salary	\N
359	Aylanma dan soliq	\N	315400		2025-08-19 00:00:00	\N	tax	income
129	bumaga	\N	15000	Kirimdan	2024-11-15 00:00:00	\N	for_office	income
124	10 L suv	\N	12000	Kirimdan	2024-11-13 00:00:00	\N	for_office	income
122	Alou wera ichimlik	\N	10000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
117	Konfet bimbom	\N	23000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
112	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	40000	Kirimdan	2024-11-25 00:00:00	\N	other_expense	income
105	Restaran aylangani chiqanda avtobus uchun	\N	8000	Kirimdan	2024-11-05 00:00:00	\N	other_expense	income
208	\N	\N	20000	\N	2024-12-23 00:00:00	14	employee_salary	\N
226	Daromad soliq	\N	357000	Yanvar oyi soliq	2025-02-25 00:00:00	\N	tax	income
236	Target yoqish uchun	\N	300000		2025-03-04 00:00:00	\N	smm_service	income
244	\N	\N	1000000	\N	2024-11-01 00:00:00	12	employee_salary	\N
246	\N	\N	1000000	\N	2025-03-19 00:00:00	22	employee_salary	\N
251	\N	\N	3000000	\N	2025-03-19 00:00:00	12	employee_salary	\N
275	\N	\N	123456	\N	2025-03-22 00:00:00	\N	employee_salary	\N
282	Target yoqish uchun	\N	300000		2025-04-02 00:00:00	\N	smm_service	income
283	\N	\N	1000000	\N	2025-03-04 00:00:00	8	employee_salary	\N
284	\N	\N	1000000	\N	2025-03-04 00:00:00	5	employee_salary	\N
254	\N	\N	1000000	\N	2025-02-10 00:00:00	19	employee_salary	\N
291	\N	\N	200000	\N	2025-04-23 00:00:00	14	employee_salary	\N
300	Choroq uzum market	\N	5418000	Smm uchun chiroq uzum nasiyadan olganimiz uchun qimmat bo'b ketti	2025-04-28 00:00:00	\N	office_item	income
301	\N	\N	1000000	\N	2025-04-04 00:00:00	8	employee_salary	\N
307	Bumaga	\N	16000		2025-05-07 00:00:00	\N	for_office	income
319	Ijtimoiy soliq	\N	289000	Ijtimoiy soliq iyun oyida to'ladim	2025-04-15 00:00:00	\N	tax	income
329	Bumaga	\N	18000		2025-06-04 00:00:00	\N	for_office	income
332	\N	\N	1300000	\N	2025-06-10 00:00:00	19	employee_salary	\N
341	\N	\N	450000	\N	2025-07-15 00:00:00	15	employee_salary	\N
345	\N	\N	1000000	\N	2025-04-04 00:00:00	3	employee_salary	\N
346	\N	\N	1000000	\N	2025-05-04 00:00:00	8	employee_salary	\N
353	Mabilogivga 	\N	650000	Suv vediosini olib bergani uchun Doniyor akaga	2025-07-30 00:00:00	\N	smm_service	income
358	Pensiya badali	\N	2600		2025-08-19 00:00:00	\N	tax	income
363	Devident soliq	\N	130000		2025-08-19 00:00:00	\N	tax	income
111	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	30000	Kirimdan	2024-11-21 00:00:00	\N	other_expense	income
209	Udinitel	\N	115000	Bahromdan	2024-11-03 00:00:00	\N	office_item	bahrom
128	2 ta 10 l suv	\N	24000	Kirimdan	2024-11-15 00:00:00	\N	for_office	income
116	Qog'oz sochiq	\N	10000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
121	Limonat barbican	\N	16000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
133	Vedio studio borishga yo'l kira	\N	30000	Kirimdan	2024-11-19 00:00:00	\N	smm_service	income
123	Vedio studio	\N	300000	Kirimdan	2024-11-12 00:00:00	\N	smm_service	income
227	INPS	\N	3000	Yanvar oyi soliq	2025-02-25 00:00:00	\N	tax	income
104	Restaran aylangani chiqanda ovqatlanish uchun	\N	40000	Kirimdan	2024-11-04 00:00:00	\N	other_expense	income
238	Tilifon paynet	\N	50000	Kirimdan	2025-03-13 00:00:00	\N	for_office	income
257	Arenda hisob raqamdan	\N	3000000	Mart oyi uchun	2025-03-20 00:00:00	\N	renting	income
255	\N	\N	200001	\N	2025-03-20 00:00:00	\N	employee_salary	\N
269	\N	\N	123456	\N	2025-03-26 00:00:00	\N	employee_salary	\N
250	\N	\N	1000000	\N	2025-03-22 00:00:00	4	employee_salary	\N
292	\N	\N	1000000	\N	2025-04-04 00:00:00	29	employee_salary	\N
293	\N	\N	450000	\N	2025-04-15 00:00:00	15	employee_salary	\N
294	\N	\N	1000000	\N	2025-04-23 00:00:00	12	employee_salary	\N
308	Motostan ga syomka harajati	\N	120000	3 ta bolani taksida ob kettim. Obet qildik. Suv ichdik. Syomkadan keyin metroda qaytik	2025-05-09 00:00:00	\N	other_expense	income
320	Aylanmadan soliq	\N	170000	Iyun oyida to'ladim	2025-04-15 00:00:00	\N	tax	income
333	\N	\N	1300000	\N	2025-06-10 00:00:00	9	employee_salary	\N
340	\N	\N	450000	\N	2025-06-15 00:00:00	15	employee_salary	\N
342	Soliq Iyun oyi uchun 	\N	542000		2025-07-15 00:00:00	\N	tax	income
344	Bumaga	\N	18000		2025-07-18 00:00:00	\N	for_office	income
348	Server 1	\N	200000		2025-07-25 00:00:00	\N	for_office	income
339	\N	\N	3000000	\N	2025-06-15 00:00:00	12	employee_salary	\N
335	\N	\N	1300000	\N	2025-05-06 00:00:00	9	employee_salary	\N
303	\N	\N	1000000	\N	2025-04-05 00:00:00	9	employee_salary	\N
285	\N	\N	1000000	\N	2025-03-01 00:00:00	9	employee_salary	\N
295	\N	\N	1000000	\N	2025-05-06 00:00:00	6	employee_salary	\N
327	\N	\N	800000	\N	2025-03-04 00:00:00	19	employee_salary	\N
354	Asadulloh dizaynerga praykt bay	\N	200000		2025-08-04 00:00:00	\N	smm_service	income
362	Jismoniy shahslar daramotidan soliq	\N	312000		2025-08-19 00:00:00	\N	tax	income
364	\N	\N	450000	\N	2025-08-19 00:00:00	15	employee_salary	\N
134	Bumaga qo'g'oz sochiq	\N	30000	Kirimdan	2024-11-21 00:00:00	\N	for_office	income
130	Qog'oz sochiq	\N	13000	Kirimdan	2024-11-15 00:00:00	\N	for_office	income
118	2 ta Pulpy suv	\N	30000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
113	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	45000	Kirimdan	2024-11-26 00:00:00	\N	other_expense	income
108	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	28000	Kirimdan	2024-11-14 00:00:00	\N	other_expense	income
106	Restaran aylangani chiqanda Yo'l-kiraga uchun	\N	24000	Kirimdan	2024-11-12 00:00:00	\N	other_expense	income
125	SSD sertifikat	\N	75000	Kirimdan	2024-11-14 00:00:00	\N	office_item	income
210	Gupka	\N	5000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
212	Arenda	\N	9100000	Bahromdan	2024-10-15 00:00:00	\N	renting	bahrom
228	Divedent soliq	\N	1190000	Yanvar oyi uchun soliq	2025-02-25 00:00:00	\N	tax	income
229	Arenda Hisob raqamdan	\N	3000000	Fevral oyi arendasi	2025-02-25 00:00:00	\N	renting	income
240	We fi to'lovi	\N	500000	Komiljon akani hisobidan to'lovga o'tib ketti	2025-03-10 00:00:00	\N	for_office	income
268	\N	\N	123456	\N	2025-03-31 00:00:00	\N	employee_salary	\N
270	\N	\N	123456	\N	2025-03-31 00:00:00	\N	employee_salary	\N
278	Bumaga	\N	18000		2025-03-21 00:00:00	\N	for_office	income
286	Target uchun	\N	300000		2025-04-06 00:00:00	\N	smm_service	income
302	\N	\N	1000000	\N	2025-04-10 00:00:00	19	employee_salary	\N
311	10 L suv	\N	14000		2025-05-15 00:00:00	\N	for_office	income
314	\N	\N	450000	\N	2025-05-16 00:00:00	15	employee_salary	\N
321	Jismoniy shahslardan daromad solig'i	\N	357000	Iyun oyida to'ladim	2025-05-15 00:00:00	\N	tax	income
324	Server 1 oylik to'lovi	\N	200000	Server ishlashi uchun to'lov	2025-06-04 00:00:00	\N	for_office	income
328	20 L suv	\N	28000		2025-05-31 00:00:00	\N	for_office	income
334	\N	\N	1300000	\N	2025-05-10 00:00:00	19	employee_salary	\N
336	Server 1	\N	200000		2025-06-30 00:00:00	\N	for_office	income
347	Soliqlar 	\N	1208000		2025-06-15 00:00:00	\N	tax	income
349	Server 2 to'lovi	\N	200000		2025-07-26 00:00:00	\N	for_office	income
351	We fi to'lovi	\N	300000		2025-06-01 00:00:00	\N	for_office	income
355	Ofisga parta	\N	340000		2025-08-14 00:00:00	\N	office_item	income
360	Ijtimoiy soliq	\N	312000		2025-08-19 00:00:00	\N	tax	income
365	Arenda to'lovi yangi ofis	\N	1260000		2025-08-20 00:00:00	\N	renting	income
220	Instagram targetga	\N	310000	Kirimdan	2025-02-13 00:00:00	\N	smm_service	income
109	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	30000	Kirimdan	2024-11-16 00:00:00	\N	other_expense	income
241	Foizga chiqib ketti	\N	4781000	Bank foizi uchun	2025-03-21 00:00:00	\N	other_expense	income
107	Restaran aylangani chiqanda ovqatlanish va yo'l kira uchun	\N	32000	Kirimdan	2024-11-13 00:00:00	\N	other_expense	income
49	Restaran aylangani chiqqanda avtobusga	\N	8000	Kirimdan	2024-11-04 00:00:00	\N	other_expense	income
153	Lipton choy ofisda yigitlarga	\N	16000	Kirimdan	2024-11-26 00:00:00	\N	for_office	income
259	Mustafoga qarzimiz	\N	1300000		2025-03-19 00:00:00	\N	other_expense	income
148	Restaran aylangani chiqqanda ovqatlanishga	\N	40000	Kirimdan	2024-11-05 00:00:00	\N	other_expense	income
149	Chelak polni yuvish uchun	\N	30000	Kirimdan	2024-11-26 00:00:00	\N	office_item	income
150	Pol latta	\N	20000	Kirimdan\n	2024-11-26 00:00:00	\N	office_item	income
151	Shakar	\N	18000	Kirimdan	2024-11-26 00:00:00	\N	for_office	income
152	Quruq choy	\N	15000	Kirimdan	2024-11-26 00:00:00	\N	for_office	income
154	Qog'oz sochiq	\N	20000	Kirimdan	2024-11-26 00:00:00	\N	for_office	income
155	Konfet BimBon	\N	26000	Kirimdan	2024-11-26 00:00:00	\N	for_office	income
156	Hodimlar bilan madaniy hordiq	\N	50000	Kirimdan	2024-11-26 00:00:00	\N	other_expense	income
158	Restaran menu	\N	200000	Bahromdan	2024-11-28 00:00:00	\N	other_expense	bahrom
160	Havo tozalagich	\N	15000	Kirimdan	2024-11-30 00:00:00	\N	for_office	income
161	Qog'oz sochiq	\N	20000	Kirimdan	2024-11-30 00:00:00	\N	for_office	income
162	Bumaga	\N	15000	Kirimdan	2024-11-30 00:00:00	\N	for_office	income
163	Katolog	\N	280000	Bahromdan	2024-12-02 00:00:00	\N	office_item	bahrom
164	Play market	\N	340000	Bahromdan	2024-12-02 00:00:00	\N	office_item	bahrom
165	we-fi internet	\N	500000	Kirimdan	2024-12-02 00:00:00	\N	for_office	income
166	Olx reklama	\N	23000	Bahromdan	2024-12-05 00:00:00	\N	smm_service	bahrom
167	Telefonga oylik to'lov	\N	100000	Bahromdan	2024-12-06 00:00:00	\N	other_expense	bahrom
168	Serverga	\N	325000	Bahromdan	2024-12-06 00:00:00	\N	for_office	bahrom
169	Arendaga	\N	6500000	Bahromdan	2024-12-10 00:00:00	\N	renting	bahrom
170	Arendaga	\N	2600000	Kirimdan	2024-12-10 00:00:00	\N	renting	income
171	Nalogka	\N	605000	Bahromdan	2024-12-12 00:00:00	\N	tax	bahrom
172	Serverga	\N	104000	Bahromdan	2024-12-12 00:00:00	\N	for_office	bahrom
173	10 L suv	\N	12000	Kirimdan	2024-12-13 00:00:00	\N	for_office	income
174	Vilajniy salfetka	\N	12000	Kirimdan	2024-12-13 00:00:00	\N	for_office	income
175	Birjaga	\N	1300000	Bahromdan	2024-12-20 00:00:00	\N	other_expense	bahrom
178	Arenda Naqt	\N	1300000	Kirimdan	2025-01-16 00:00:00	\N	renting	income
181	10 l suv	\N	14000	Kirimdan	2025-01-31 00:00:00	\N	for_office	income
180	Arenda naqt qolgani	\N	4800000	Kirimdan	2025-01-27 00:00:00	\N	renting	income
119	Havo tozalagich (Ozijitil)	\N	16000	Kirimdan	2024-11-12 00:00:00	\N	for_office	income
114	Musir chelak	\N	30000	Kirimdan	2024-11-06 00:00:00	\N	for_office	income
182	10 L suv	\N	14000	Kirimdan	2025-02-04 00:00:00	\N	for_office	income
179	Bank hizmati chek daftar	\N	40000	Kirimdan	2025-01-27 00:00:00	\N	tax	income
126	Serverga oylik to'lov	\N	200000	Kirimdan	2024-11-14 00:00:00	\N	for_office	income
187	\N	\N	3000000	\N	2024-12-23 00:00:00	12	employee_salary	\N
188	\N	\N	3000000	\N	2025-01-23 00:00:00	12	employee_salary	\N
131	we-fi internet	\N	500000	Kirimdan	2024-11-11 00:00:00	\N	for_office	income
356	S3 server to'lovi	\N	50000		2025-08-15 00:00:00	\N	for_office	income
26	Bumaga	\N	10000	Kirimdan	2024-11-04 00:00:00	\N	for_office	income
33	Limanad Barbican	\N	16000	kirimdan	2024-11-04 00:00:00	\N	for_office	income
159	Vizitka	\N	40000	Bahromdan	2024-11-28 00:00:00	\N	office_item	bahrom
177	Arendaga Hisob raqamdan	\N	3000000	Kirimdan	2025-01-24 00:00:00	\N	renting	income
213	We fi oylik to'lov	\N	500000	Kirimdan	2025-02-07 00:00:00	\N	for_office	income
191	\N	\N	1000000	\N	2025-01-31 00:00:00	3	employee_salary	\N
192	\N	\N	1500000	\N	2025-01-31 00:00:00	11	employee_salary	\N
193	\N	\N	1500000	\N	2025-01-31 00:00:00	18	employee_salary	\N
194	\N	\N	1000000	\N	2024-12-11 00:00:00	13	employee_salary	\N
195	\N	\N	1500000	\N	2025-01-31 00:00:00	20	employee_salary	\N
196	\N	\N	1000000	\N	2025-01-12 00:00:00	19	employee_salary	\N
197	\N	\N	100000	\N	2024-11-28 00:00:00	14	employee_salary	\N
198	\N	\N	200000	\N	2024-12-25 00:00:00	14	employee_salary	\N
199	\N	\N	200000	\N	2025-01-27 00:00:00	14	employee_salary	\N
200	\N	\N	450000	\N	2024-12-14 00:00:00	15	employee_salary	\N
201	\N	\N	450000	\N	2025-01-27 00:00:00	15	employee_salary	\N
214	10 L suv	\N	14000	Kirimdan	2025-02-05 00:00:00	\N	for_office	income
215	Bolalarga 2 ta Cola	\N	40000	Kirimdan	2025-02-05 00:00:00	\N	other_expense	income
216	100 L suv	\N	75000	Kirimdan	2025-02-06 00:00:00	\N	for_office	income
217	Tilifonga oylik to'lov	\N	50000	Kirimdan	2025-02-07 00:00:00	\N	for_office	income
218	Olx reklama	\N	30000	Kirimdan	2025-02-07 00:00:00	\N	smm_service	income
219	Serverga Oylik to'lov	\N	110000	Kirimdan	2025-02-13 00:00:00	\N	for_office	income
361	Aylanmadan soliq o'tkan oy uchun	\N	356000		2025-08-19 00:00:00	\N	tax	income
247	\N	\N	1000001	\N	2025-03-19 00:00:00	\N	employee_salary	\N
186	\N	\N	2000001	\N	2024-11-23 00:00:00	\N	employee_salary	\N
272	\N	\N	123456	\N	2025-03-22 00:00:00	\N	employee_salary	\N
287	Bumaga	\N	16000		2025-04-22 00:00:00	\N	for_office	income
304	Cup cat mantaj uchun oylik to'lov	\N	95000	Mandaj uchun kerak oylik to'lovi bu	2025-05-06 00:00:00	\N	smm_service	income
309	Smm confort prayktga borganda harajat	\N	100000	Yo'l kira obet qaytish	2025-05-10 00:00:00	\N	other_expense	income
312	Bumaga	\N	16000		2025-05-15 00:00:00	\N	for_office	income
337	Server 2	\N	200000	Iyun oyi uchun server to'lovi	2025-06-30 00:00:00	\N	for_office	income
343	Ofisga 20 l suv	\N	28000		2025-07-18 00:00:00	\N	for_office	income
350	We fi to'lovi	\N	300000		2025-05-01 00:00:00	\N	for_office	income
\.


--
-- Data for Name: incomes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.incomes (id, name, real_price, pay_price, date_paied, "position", project_id, type, description) FROM stdin;
106	\N	\N	1270000	2025-07-01 00:00:00	\N	10	from_project	Sayt uchun Avans 
107	\N	\N	2600000	2025-07-30 00:00:00	\N	9	from_project	Support puli
108	Yusufbek	1500000	1500000	2025-02-15 00:00:00	Frontent	\N	from_student	
109	\N	\N	1900000	2025-08-04 00:00:00	\N	7	from_project	Onepc support puli
83	Diyordan qarz		391300	2025-04-29 00:00:00		\N	investor	
78	\N	\N	2600000	2025-04-02 00:00:00	\N	9	from_project	Prayekt puli
79	\N	\N	1950000	2025-03-25 00:00:00	\N	7	from_project	Support puli 150$
80	Bahtiyor	1500000	1500000	2025-04-02 00:00:00	Frontend 	\N	from_student	
4	Dilshodov Abdurashid	1200000	1200000	2024-10-08 00:00:00	front-end	\N	from_student	\N
16	\N	\N	1300000	2025-02-06 10:27:33.777942	\N	10	from_project	\N
82	Abdurauf	1500000	1950000	2025-04-04 00:00:00	Frontend	\N	from_student	
5	Dilshodov Abdurashid	1300000	1300000	2024-11-08 00:00:00	front-end	\N	from_student	\N
84	Oybek Mikrafon uchun 		391300	2025-04-29 00:00:00		\N	investor	
85	Oybek Chiroq uchun		1806000	2025-04-28 00:00:00		\N	investor	
86	Oybek arenda uchun qarz onamdan		6500000	2025-04-29 00:00:00		\N	investor	
87	\N	\N	2600000	2025-04-29 00:00:00	\N	33	from_project	Birinchi oy to'lovni 50%
88	\N	\N	1950000	2025-04-30 00:00:00	\N	7	from_project	Support puli
89	\N	\N	2600000	2025-05-01 00:00:00	\N	33	from_project	Oylik to'lovi ikkinchi yarmi
90	Abdurauf	1500000	1500000	2025-05-04 00:00:00	Frontend 	\N	from_student	
91	\N	\N	2500000	2025-05-08 00:00:00	\N	34	from_project	3 oy davomida har oy 200$ dan to'lov qiladi
110	\N	\N	1250000	2025-08-18 00:00:00	\N	10	from_project	100$ 3 chi qismi yana 100$ qoldi
38	Diyordan qarz		1500000	2024-11-23 00:00:00		\N	investor	
60	Oybek qarz		16312000	2025-03-19 00:00:00		\N	investor	
81	Oybek		1068000	2025-04-02 00:00:00		\N	investor	
17	\N	\N	300000	2025-01-16 00:00:00	\N	11	from_project	
18	\N	\N	300000	2025-01-16 00:00:00	\N	12	from_project	
92	\N	\N	1300000	2025-05-15 00:00:00	\N	35	from_project	Avas yana 2600000 beradi
35	Bahromdan		9960500	2024-10-31 00:00:00		\N	investor	
37	Bahromdan		11102000	2024-12-31 00:00:00		\N	investor	
42	\N	\N	7800000	2025-01-31 00:00:00	\N	6	from_project	Prayektni 50% puli
93	\N	\N	1300000	2025-05-15 00:00:00	\N	36	from_project	50% avansni berdi yana 1300000 beradi
48	\N	\N	2600000	2024-10-15 00:00:00	\N	7	from_project	One PC avans
111	\N	\N	2600000	2025-08-19 00:00:00	\N	34	from_project	Xeo xizmati 3 oy to'lovi
50	\N	\N	500000	2024-11-11 00:00:00	\N	7	from_project	We fe to'lovi uchun o'tkazildi
51	\N	\N	500000	2024-12-12 00:00:00	\N	7	from_project	We fi to'lovi uchun o'tkazildi
52	\N	\N	500000	2025-01-11 00:00:00	\N	7	from_project	We fi to'lovi uchun o'tkazildi
53	\N	\N	500000	2025-02-11 00:00:00	\N	7	from_project	We fi to'lovi uchun o'tkazildi
1	Yusfbek Hamidullayev	1500000	1500000	2024-12-18 00:00:00	Frontend	\N	from_student	soqqa
14	\N	\N	23500000	2025-02-06 00:00:00	\N	8	from_project	
112	\N	\N	1260000	2025-08-20 00:00:00	\N	38	from_project	Birinchi oy 50% to'lovi
94	Onamdan qarz		1700000	2025-06-04 00:00:00		\N	investor	
55	\N	\N	7800000	2025-02-25 00:00:00	\N	6	from_project	Qolgan 50% puli
45	Abdurauf	1500000	1800000	2025-03-02 00:00:00	Front-end 	\N	from_student	
46	Bahtiyor	1500000	1400000	2025-02-17 00:00:00	Front-end 	\N	from_student	
56	\N	\N	500000	2025-03-10 00:00:00	\N	7	from_project	We fi uchun to'landi
95	Boburdan qarz		2000000	2025-06-04 00:00:00		\N	investor	
96	\N	\N	1935000	2025-06-04 00:00:00	\N	7	from_project	One pc support puli
97	\N	\N	2600000	2025-05-30 00:00:00	\N	9	from_project	Motostan support puli
98	\N	\N	2500000	2025-06-10 00:00:00	\N	35	from_project	200$ berdi 
99	Onamdan qarz		13000000	2025-06-10 00:00:00		\N	investor	
100	\N	\N	1900000	2025-07-01 00:00:00	\N	7	from_project	One support 3 oy puli
101	\N	\N	2600000	2025-07-15 00:00:00	\N	9	from_project	Iyun oyi support 2 oy uchun to'lov
102	\N	\N	4200000	2025-07-18 00:00:00	\N	37	from_project	Birinchi oy hizmat uchun 33% o'tkazildi
103	\N	\N	2600000	2025-07-18 00:00:00	\N	34	from_project	Seo hizmatimiz uchun 2 oy to'lovi
104	\N	\N	1270000	2025-07-23 00:00:00	\N	10	from_project	2 to'lovni qildi.
2	Hamidullayev Yusufbek	1500000	1500000	2024-11-17 00:00:00	front-end	\N	from_student	\N
\.


--
-- Data for Name: login_pass_note; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login_pass_note (id, login, password, name) FROM stdin;
\.


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.message (id, chat_id, sender_id, content, created_at) FROM stdin;
1	1	6	string	2025-04-10 13:55:06.025643
2	1	4	what my man	2025-04-10 13:55:28.654135
3	2	6	string	2025-04-10 15:11:42.054967
4	1	4	asdas	2025-04-11 12:52:53.5537
5	1	4	asdsadasd	2025-04-11 12:53:09.36799
6	1	6	asdasd	2025-04-11 12:53:35.251928
7	1	4	asdasdasd	2025-04-11 12:56:07.094549
8	1	6	.	2025-04-11 13:03:10.883695
9	1	4	asdasd	2025-04-11 13:13:43.280367
10	1	4	asdasd	2025-04-11 13:16:19.709511
11	1	6	aaaaa	2025-04-11 13:17:15.551229
12	1	4	asdasd	2025-04-11 13:18:42.432984
13	1	6	Shahzoq qale	2025-04-11 13:19:01.205114
14	1	4	Tinch	2025-04-11 13:19:55.091541
15	1	6	asdasda	2025-04-11 13:20:01.007519
16	1	4	gsadfsgsd	2025-04-11 13:20:16.265512
17	1	4	asdfasdf	2025-04-11 13:24:01.376234
18	1	4	asdasd	2025-04-11 13:24:05.843848
19	1	4	...	2025-04-11 13:24:11.046344
20	1	4	🫠😉	2025-04-11 13:45:02.323775
21	1	4	😆😅	2025-04-11 13:46:36.008412
22	1	4	✊🏿	2025-04-11 13:47:10.944457
23	1	4	x	2025-04-11 13:48:14.558688
24	1	4	asdas\nsdfsd\n	2025-04-11 13:48:59.277777
25	1	4	asdasdasd	2025-04-11 13:54:46.870711
26	1	4	asdas	2025-04-11 13:54:49.066737
27	1	4	asdasd	2025-04-11 13:54:50.127157
28	4	3	salom	2025-04-11 13:59:08.335111
29	4	6	Qale	2025-04-11 13:59:12.261606
30	4	3	nima gap 	2025-04-11 13:59:13.183948
31	4	3	😝	2025-04-11 13:59:21.654551
32	4	6	🗣️	2025-04-11 13:59:42.309762
33	4	3	🥂🥂🥂🥂🥂	2025-04-11 14:00:02.074008
34	4	6	🤟🏾	2025-04-11 14:00:05.962181
35	4	3	👍	2025-04-11 14:00:26.364569
36	1	4	what is up bro	2025-04-11 14:01:07.810762
37	4	3	sxasxas	2025-04-11 14:01:34.594431
38	1	6	...	2025-04-11 14:01:54.870013
39	1	4	as	2025-04-11 14:01:57.928246
40	1	6	Ass	2025-04-11 14:02:02.80099
41	1	4	hack the pentagon	2025-04-11 14:02:05.916877
42	1	4	🫠	2025-04-11 14:02:16.56485
43	1	4	🌰🌰🌰🌰🌰🌰🌰🌰🌰🌰🌰🌰	2025-04-11 14:02:23.774659
44	1	3	salom	2025-04-11 14:02:37.630656
45	1	3	man behruz	2025-04-11 14:02:44.966815
46	1	4	men odamman	2025-04-11 14:03:17.097079
47	1	4	sd	2025-04-11 14:03:28.043593
48	1	4	sdf	2025-04-11 14:03:28.246143
49	1	4	s	2025-04-11 14:03:28.488354
50	1	4	df	2025-04-11 14:03:28.615005
51	1	4	sd	2025-04-11 14:03:28.761394
52	1	4	fs	2025-04-11 14:03:28.872638
53	1	4	df	2025-04-11 14:03:29.059821
54	1	4	s	2025-04-11 14:03:29.17719
55	1	4	df	2025-04-11 14:03:29.291831
56	1	4	sdfsdf	2025-04-11 14:03:29.887389
57	1	4	sf	2025-04-11 14:03:30.011212
58	1	4	s	2025-04-11 14:03:30.207003
59	1	4	f	2025-04-11 14:03:30.308564
60	1	4	s	2025-04-11 14:03:30.496421
61	1	4	f	2025-04-11 14:03:30.583878
62	1	4	sd	2025-04-11 14:03:30.721052
63	1	4	f	2025-04-11 14:03:30.801299
64	1	4	sd	2025-04-11 14:03:31.029407
65	1	4	fs	2025-04-11 14:03:31.112745
66	1	4	df	2025-04-11 14:03:31.23451
67	1	4	s	2025-04-11 14:03:31.431614
68	1	4	dfsdf	2025-04-11 14:03:31.881864
69	1	4	s	2025-04-11 14:03:31.933041
70	1	4	fd	2025-04-11 14:03:32.037611
71	1	4	s	2025-04-11 14:03:32.130975
72	1	4	df	2025-04-11 14:03:32.245143
73	1	4	s	2025-04-11 14:03:32.446994
74	1	4	fd	2025-04-11 14:03:32.648007
75	1	4	sdf	2025-04-11 14:03:32.856804
76	1	4	sd	2025-04-11 14:03:32.976321
77	1	4	fs	2025-04-11 14:03:33.166803
78	1	4	df	2025-04-11 14:03:33.256237
79	1	4	s	2025-04-11 14:03:33.471489
80	1	4	df	2025-04-11 14:03:33.571738
81	1	4	sd	2025-04-11 14:03:33.703471
82	1	4	f	2025-04-11 14:03:33.809893
83	1	4	s	2025-04-11 14:03:33.998717
84	1	4	f	2025-04-11 14:03:34.088032
85	1	4	sd	2025-04-11 14:03:34.180727
86	1	4	f	2025-04-11 14:03:34.296848
87	1	4	sd	2025-04-11 14:03:34.41318
88	1	4	f	2025-04-11 14:03:34.505625
89	1	4	sf	2025-04-11 14:03:34.602334
90	1	4	s	2025-04-11 14:03:34.805469
91	1	4	f	2025-04-11 14:03:34.898324
92	1	4	sd	2025-04-11 14:03:35.004222
93	1	4	f	2025-04-11 14:03:35.116944
94	1	4	sdf	2025-04-11 14:03:35.361052
95	1	4	sd	2025-04-11 14:03:35.525229
96	1	4	f	2025-04-11 14:03:35.63457
97	1	4	sd	2025-04-11 14:03:35.758553
98	1	4	f	2025-04-11 14:03:35.856549
99	1	4	sd	2025-04-11 14:03:36.0305
100	1	4	f	2025-04-11 14:03:36.125
101	1	4	sd	2025-04-11 14:03:36.231859
102	1	4	f	2025-04-11 14:03:36.359392
103	1	4	sd	2025-04-11 14:03:36.459343
104	1	4	f	2025-04-11 14:03:36.558903
105	1	4	sfdsf	2025-04-11 14:03:36.975087
106	1	4	sf	2025-04-11 14:03:37.155603
107	3	4	what bro	2025-04-11 14:05:39.633223
108	4	3	zor	2025-04-11 14:07:49.479823
109	1	4	asd	2025-04-11 14:14:29.756088
110	1	6	sfsdfsdfs	2025-04-12 14:59:19.539785
111	1	4	qwertyj	2025-04-14 12:13:37.509905
112	1	4	😇😗	2025-04-14 12:14:19.018934
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, message, created_at, is_read) FROM stdin;
\.


--
-- Data for Name: operator_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.operator_type (id, name) FROM stdin;
1	Mijozlar
2	Sotuv menejeri
3	Ehtimoliy hodimlar
4	Ehtimoliy mijoz kompaniyalar
\.


--
-- Data for Name: operators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.operators (id, full_name, phone_number, description, status, operator_type_id) FROM stdin;
21	Elbrus	956052222	Barcha xizmati bor ekan. Telegram bot kerak emas ekan mijozlari faqat telefon qilib zakaz berishar ekan telegram botga o'rganmapdi\n\nWeb sayt bor. telefon raqami noto'g'ri\n	cancel	4
59	Otabek CRM	943238489	Seshanba 2 3 larda narx taklifini aytish kerak\n\nDushanba kuni 07.04.2025 qayta aloqaga chiqish kerak\n\nQurilish mollari uchun CRM tizimi kerak ekan\n	cancel	1
45	"HOT CRUCH" xususiy korxonasi	+998917980601	Ovqаtlаnishni tаshkil qilishning boshqа turlаri	empty	4
71	"EB SOCIETE"  MCHJ	951205737	Ixtisoslаshmаgаn ulgurji sаvdo	empty	4
68	"MONOLITH JARKURGAN" MCHJ	908239900	Turаr joy binolаrini qurish	empty	4
24	Crystal ( Pure water )	881469999	Barcha xizmat o'zida bor ekan\n\nOfisini borib topolmadik	cancel	4
69	"ACTIVE ASSETS" MCHJ	901147325	Ixtisoslаshmаgаn ulgurji sаvdo	empty	3
40	"MAXMUDOTA TREDING" MCHJ	+998943589590	Boshqа toifаlаrgа kiritilmаgаn shаxsiy xizmаtlаr	empty	4
41	"FLEET CORE" MCHJ	+998909005554	Mа'lumotlаrni joylаshtirish vа ishlov berish bo'yichа xizmаtlаr	empty	4
81	"ALUTECH CABLE" MCHJ	903537504	Xizmat doirasidan tashqarida\nIxtisoslаshmаgаn ulgurji sаvdo	empty	4
26	Ixtiyor ( ICE BERG )	900920322	Bizdan oldin boshqa kompaniya aloqaga chiqqan ekan o'shalar bilan ishlaydigan bo'lishibdi\nDushanba kuni ko'rishib gaplashib olamiz. CRM tizimi kerak asosan\nBirinchi telefonni ko'tarmadi\n\nMalumot yo'q\nYana raqami: 55 500 88 87	cancel	4
80	Poytaxt water	884004500	Hozircha qiziqtirmas ekan\nYozganimni o'qib javob yozmagan ekan yena yozib yubordim\nTelegramdan ma'lumotlarni tashlab qo'ydim\nSayt bor bot yo'q\n	cancel	4
42	"USMANOV PRODUCTION N1" MCHJ	+998946564646	Boshqа toifаlаrgа kiritilmаgаn shаxsiy xizmаtlаr	empty	4
20	Enjoy water	+998950809070	o'zini IT xizmatchisi bor ekan. \nTelegram boti bor @enjoywaterbot	cancel	4
43	"NEW TRUST SERVICE" MCHJ	+998998960234	Ob'ektlаrgа kompleks xizmаt ko'rsаtish	empty	4
148	Daily water	975010023	Farg'onada\nIntagiram 4.528 ta \nTelegiram bot yo'q\nWeb sayt yo'q	empty	4
19	Zilol	+998951442066	Bu xizmatlar kerakmas hozir dedi\n\nBir xaftadan keyin aloqaga chiqish kerak (28.04) Rahbari turkiyada ekan hali kelmagan ekan\n\nIkki haftadan keyin qayta oloqaga chiqish kerak. 21.04.2025 sanada aloqaga chiqish kerak. Hich nima maʼlum emas	cancel	4
66	"ETOILE GROUP" xususiy korxonasi	917747275	Quruqlik trаnsporti sohаsidаgi xizmаtlаr	empty	4
22	Do'rmon suv	+998983606600	Malumot tashlab qo'ydim. telefonim o'chib qoladi dedi, malumot tashlab qo'ying dedi\n	cancel	4
60	Vital water	998048080	O'zini IT xizmatchilari bor ekan\n\nTelefonni ko'tarmadi\nBot bor sayt yo'q\n\n	cancel	4
17	Arctic	937770056	Telegiram bot yo'q. Web sayt yo'q. Ofisiniyam topa olmadik.\nIkkinchi raqam: 93 777 55 95	empty	4
73	"MIXPAPER" MCHJ	974411177	Qog`oz vа kаrtondаn boshqа buyumlаr ishlаb chiqаrish	empty	4
27	Furat water	930462020	Barcha xizmatlari bor ekan to'xtatib qo'ygan ekan\n\nMalumot yo'q \nYana raqamlari: \n93 047 20 20	cancel	4
62	City water	933845995	Boshqalarni xizmatidan foydalanayotgan ekan\nTelegram bot yo'q sayt yo'q\n	cancel	4
67	"BAIYILIHAO CONSULTING" mas`uliyati cheklangan jamiyati qo'shma korxonasi	909483777	Tijorаt fаoliyati vа boshqаruv mаsаlаlаri bo'yichа mаslаhаt berish	empty	4
6	Ezoza	930648377	@ezozeezozv\nkino\n	cancel	4
118	Shabnam water	991003200	Rustam-973331776\n\nYakshanba aloqaga chiqish kerak\n\n Sayt yo'q bot yo'q	in_progres	4
63	"INFIN ESTATE CONSULTING" Mchj	997896666	Boshqа toifаlаrgа kiritilmаgаn, xo'jаlik fаoliyatigа yordаmchi xizmаt ko'rsаtishning boshqа turlаri	empty	4
64	"SOLIH-PLAST" MCHJ	977025604	Boshqа plаstmаssа buyumlаr ishlаb chiqаrish	empty	4
16	Soft water	973020202	Feruz Dawylife Water ni sherigi\nTelefonni ko'tarmadi \n\nTelegiram bot yo'q. Web sayt yo'q. \nIkkinchi raqami: 93 178 45 51	cancel	4
11	Biolife water	555002555	Bot bor web sayt ham bor taklif berib ko'rish kerak. Ofisini topa olmadik.	empty	4
70	"MARKWOOD" MCHJ	998976129	Boshqа mebellаr ishlаb chiqаrish	empty	4
65	"CHEF SWEETS" MCHJ	998273130	Ixtisoslаshmаgаn do'konlаrdа boshqа tovаrlаr chаkаnа sаvdosi	empty	4
74	"ZHONG YA TRAVEL" MCHJ	935900710	Turistik аgentliklаr fаoliyati	empty	4
75	"HINDUKUSH"  MCHJ	900966884	Yashаsh uchun mo'ljаllаnmаgаn binolаr qurish	empty	4
76	"XON TRUST" MCHJ	998282984	Ixtisoslаshmаgаn ulgurji sаvdo	empty	3
78	"CHANG SHA FAN DIAN"  MCHJ	996664853	Ovqаtlаnishni tаshkil qilishning boshqа turlаri	empty	4
79	"FAZO PREMIUM" MCHJ	998024438	Ixtisoslаshmаgаn ulgurji sаvdo	empty	4
82	"TETSU"  MCHJ	996161818	Spirtsiz ichimliklаr ishlаb chiqаrish; butilkаdа minerаl suvlаr vа boshqа suvlаr ishlаb chiqаrish	empty	4
61	Gumus su	900122414	Boshqa telefon qilmang dedi\n\nTelefonni ko'tarmadi\nxizmat doirasidan tashqarida\nBot bor. sayt yo'q\n	cancel	4
84	"BASTION BUILD" MCHJ	903240220	Turаr joy binolаrini qurish	empty	4
86	"ANSOR HELPER" MCHJ	908084395	Boshqа toifаlаrgа kiritilmаgаn shаxsiy xizmаtlаr	empty	4
87	"SHUAIB ALIMI"  MCHJ	955714607	Ixtisoslаshmаgаn do'konlаrdа boshqа tovаrlаr chаkаnа sаvdosi	empty	4
111	Extreme water	974247024	hamma narsasi bor ekan\n\n974247024 / 996888688	cancel	4
83	Ideal water	712008118	Hammasi bor	empty	4
28	Agat water	712030606	Boshliqlariga telefon raqamimizni berar ekan\nHozircha malumot yoʻq \nYana raqamlari: \n99 819 06 06	cancel	4
112	Imkon water (Suvel water)	917979999	O'iz aloqaga chiqar ekan \nSEO ni taklif qilish kerak\nSayt bor, bot bor\n71-200-200-8\n91-797-9999	cancel	4
72	"ELNA" MCHJ	993071048	Boshqа kiyimlаr vа аksessuаrlаr ishlаb chiqаrish	empty	4
85	ADEL premium water	992366159	Kerak bo'lsa o'zi aloqaga chiqar ekan\n\n\nTelegramdan taklifni yozib yubordim\nxech nima yo'q\n	cancel	4
126	Mone water	90 3338000	TK\n\nXizmat doirasidan tashqarida\nXizmat doirasidan tashqarida\n\nTelefonni ko'tarmadi\nTelefonni ko'tarmadi\n\nhttps://glotr.uz/mineralnaya-voda-zam-zam-p-702234/\n\nhttps://www.yellowpages.uz/kompaniya/mone-water-pitevaya-voda\n\nX	in_progres	4
89	"ENGRAVE" MCHJ	973685775	Boshqа mаishiy tovаrlаr ulgurji sаvdosi	empty	4
98	"BUETYBAY" MCHJ	946717774	Pochtа vа Internet orqаli chаkаnа sаvdo	done	4
91	"MAX PRODUC" MCHJ	951430010	Ixtisoslаshmаgаn ulgurji sаvdo	empty	4
131	Selva	999023333	Telegramdan taklifni yuborib qo'ydim\n\n\nTelegramdan taklifni tashlab qo'yish ekrak\n\nSayt bor bot yo'q\n	cancel	4
94	"LAZIZBEK DELFIN" MCHJ	888605868	Restorаnlаr vа oziq-ovqаt mаhsulotlаri etkаzish bo'yichа xizmаtlаr	empty	4
77	Quduq water	903339993	Telefonni ko'tarmadi\n\nNommer operatordan olingan\nsayt bor bot yo'q\n\n	cancel	4
93	"ORO TECH"  MCHJ	901876747	Ixtisoslаshmаgаn ulgurji sаvdo	empty	4
95	"CHINA MASTERPRO"  MCHJ	889727271	Ixtisoslаshmаgаn ulgurji sаvdo	empty	4
96	"ELEKTRON HISOBLAGICH TRADE" MCHJ	992255255	Elektron vа telekommunikаtsion uskunаlаr vа ulаrning ehtiyot qismlаri ulgurji sаvdosi	empty	4
97	"POLYMER DYNAMICS" MCHJ	900918515	Boshqа plаstmаssа buyumlаr ishlаb chiqаrish	empty	3
100	"STROY EAT" MCHJ	935205026	Turаr joy binolаrini qurish	empty	4
102	"MEGA INTER TEKS " MCHJ	909793900	To'qilgаn vа trikotаj polotno ishlаb chiqаrish	empty	3
124	Gidrosfera water	944686666	Xumoyun - 944646666\n\nMobil ilova uchun taklif ishlab chiqish kerak. mobil ilovada CRM + Bot funksiyalari bo'lishi kerak\nQayerga borish kerak, qayerda nechta kapsula bor shularni ham barchasini ko'rsatish kerak	in_progres	4
134	Aqualife	950775511	CRM ni bollarga aytishar ekan. o'ylab ko'rib aloqaga chiqishar ekan\n\nTelefonni ko'tarmadi\n97 6650909- Bahodir\n\nSayt bor bot yo'q	cancel	4
127	"A R LOGO" MCHJ	958999111	Sog`liqni sаqlаsh sohаsidаgi boshqа fаoliyat	empty	4
114	Chimgan water	781503000	BOT + sayt\nish boshlandi\n\n10.04 telefon qilib nima bo'ldi so'rash kerak.\n\n09.04.2025 kuni abetdan keyin uchurashuv belgilandi\n\nUlug'bek degan odam rahbari ekan\n\n970340138-Xilola\n	done	4
141	Cleanwater Azamat	886209999	Boshqa kompaniya bilan shartnoma qilishgan ekan qilgan crm tizimlarimizni videoga olib tashlab qoʻying dedi\n\nBir haftalardan qayta aloqaga chiqish kerak(28.04) rahbari kelishi kerak ekan qo'shimcha Telegramdan ma'lumot tashlab qo'ydim telegramda yozishganmiz\n\nTelefonni ko'tarmadi\nTelegiram bot yo'q\nWeb sayt bor	cancel	4
103	"VENTSHOP" MCHJ	771316656	ventstore.uz lakatsiyasi saytida bor \n\nIxtisoslаshmаgаn ulgurji sаvdo	empty	4
117	El Clasico	781503003	Oʻzini Aytishnigi borakan\n\nOperatori bilan gaplashdim rahbari xitoyga kamandirofkaga ketgan ekan 1 hafta 10 kunda habar olish kerak (23.05)10kun bo'ladi\n\noperator bilan gaplashdim rahbari hali kelmagan ekan. haftani oxirlariga xabar olish kerak\n\n10 kundan keyin (20.04) habar olish kerak.\noperatori bilan gaplashdim, rahbarlari chetga chiqib ketishgan ekan. Ismimni yozib oldi.\n\nSayt bor bot yo'q	cancel	4
138	Salohiddin Mavi toshkent	774030808	Erta yoki indin telefon qilib xabar olish kerak. nima bo'ldi gaplashib ko'rdimi yo'qmi. o'zim bir borib tushuntirib bersam yenada tushunarli bo'lardi deyish kerak\n\nbot bor sayti yo'q	cancel	4
123	Sharshar water	770154147	Hamma xizmati bor ekan\nTelefonni ko'tarmadi 2\n\n17:00 da tel qilish kerak\nXech nimasi yo'q	cancel	4
147	Grandwater	979199393	Farhod - 915219900 telefonni ko'tarmadi\n\nInstagiram 21.500 obunachi\nbot yo'q \nWeb sayt bor	cancel	4
145	Dafane water	901097222	Telefonni ko'tarmadi\nPirmat aka - 880507771 nommerini operatoridan oldim\n\nTelefonni ko'tarmadi\nInstagiram 1352 ta obunachi\nTelegiram bot yo'q\nWeb sayt yo'q	cancel	4
23	Ibrohim Marwa	990803399	telegramdan ma'lumot tashlab qo'ydim hali javob kelmadi\n\ntelefonni ko'tarmadi\n\npayshanba kuni aloqaga chiqish kerak\n10.04.2025 payshanba kuni bo'sh bo'laman ungacha ko'risha olmasam kerak degan edi\n	cancel	4
119	Hayot water	909110077	995159182-Erkinbek\nNommerini operatoridan oligan\nhayotwater.uz	cancel	4
122	Zilha water	330255050	Nommer boshqa ekan\n\n\nXech nima yo'q	in_progres	4
132	Royal	770983333	Telefonni ko'tarmadi\n\nYoʻlda ekan 1 soatlarda tel qilish kerak 17:00\n\nTelefonni ko'tarmadi\nKamoliddin - 935542002\nNommerini operatordan olinganini aytmaslik kerak\n\nkeyinroq telefon qilish kerak. 5 daqiqa vaqtingiz bormi deganimda tezroq dedi va ishi borligi uchun keyinroq telefon qiling dedi.\n\ntel qilganda \nbiz nima bilan shug'ullanishimiz va kompaniya haqida ma'lumot berish kerak\n\nXech nimasi yo'q	in_progres	4
139	Dua premium water	906989999	Kompaniya haqida ma'lumot berdim telegramdan ham ma'lumoto tashlab qo'ydim. menejerlarimizga telefon raqamingizni beramiz o'zlari aloqaga chiqadi deyishdi. bor bot web sayti yo'q	cancel	4
133	Eco life	991978694	Hozirlikcha kerak emas deyapti\n\nxizmat doirasidan tashqarida\n\nXech nimasi yo'q	cancel	4
140	Musaffo suv Nodira	972099999	Hozir bu jarayonda CRM ustida ishlayapmiz 2 martta borib keldim\n\nAsosan CRM ga qiziqish bildirdi telegramdan ma'lumot tashlab berdim\nInstagiram 10,600 obunachi \nTelegiram bot bor	cancel	4
143	Nest water	959543302	Instagiram profili faol 116 ta obunachi \nTelegiram bot yo'q\nWeb sayt yo'q	empty	3
135	Obi Zam Rovshan	88 543 88 88	Telegramda yozishganlarimizni o'chirib tashlagan ekan\n\ntelegramdan yozib qo'ydim\n\nXech nimasi yo'q	cancel	4
142	Toyyiba water	977457755	Telegramdan lakatsiya tashlab qo'yish kerak vaqatimga qarab o'taman dedi\n\nErtaga telefon qilish kerak 14.05\n\nTelefonni ko'tarmadi\nTelegiram bot \nWeb sayt topilmadi.\n	in_progres	4
115	Crystall life water	998660497	Taklifni yozma ravishda jo'natib qo'ydim\n\nTaklifni yozma ravishda tayyorlab jo'natish kerak\n\nXEch nima yo'q	cancel	4
149	Eleven Toshkent suvlari	993020011	Barcha narsasi bor	empty	4
58	Nurali	977075718	Telefonini ko'tarmadi 3\n\nIp-telefoniya kerak ekan. Dushanba kuni 07.04.2025 da meet oraqali gaplashish kerak soat 11:00 dan 14:00 gacha bo'lgan vaqt oralig'ida telefon qilish kerak\n\n\n	empty	1
99	"HUSMA TOURS" MCHJ	903502305	Turistik аgentliklаr fаoliyati	done	4
110	Аqua DELUX Water	941236663	yakshanba kuni aloqaga chiqishar ekan\nXech narx yo'q\n	cancel	4
101	"MEROS SAROY" MCHJ	935509041	Turаr joy binolаrini qurish	empty	4
137	Aqua ice	959510033	Mijozlari yetarli ekan ko'pi zo'riqtirib gemaroyi chiqishiga sabab bo'larkan\n\n991290033- Dilmurod\n\nBot bor sayt yo'q\n	cancel	4
128	simma water	770017777	Hammasi bor ekan yasatayotgan ekan\n774088885- Muhammadyusuf\n Bot bor sayt yo'q	cancel	4
166	COOL WATER SERVICE	(95) 194-07-57	Raqami noto'g'ri\nX	empty	4
158	Royal gold water	911323041	Raqam noto'g'ri\n	empty	4
160	Safo water	886661111	X Farg'onada ekan	empty	4
125	OASIS water	712005515	Buxoroda X	empty	4
170	HUB WATER	977148816	Raqamga qo'ng'iroq qilib bo'lmaydi deyapti\nX	empty	4
136	Aquasoff	991400999	Akasi bilan gaplashibdi akasi hozircha kerak emas degan ekan\n\nAkasi xorazimdan kelishi kerak ekan xaftani oxirlarida bir xabar olish kerak (26.04)\n\nErta yoki indin ofisingizga o'taman degan\n16.04 yoki 17.04 da telefon qilib. aka nima bo'ldi kela olasizmi yoki o'zim boraymi deyish kerak\n\nTelefonni ko'tarmadi\nhammasi bor lekin ishlamaydi\n	cancel	4
152	Enjoy water	950809070	Aytishnik ishga olingan ekan sayti endi ishga tushayotgan ekan\nTelegram bot bor sayt yo'q	cancel	4
57	Mushtari BRILLIANT PURE WATER	99 0993113 	Crm tizimi o'chib ketibdi. Eski CRM tizimi yaxshi ishlamagan ekan. deyarli eplab o'rnatib ham berishmagan ekan.\n\nGaplashdim hozir tashlab beraman dedi\n\nErtalab 10 larda tel qilish kerak\nertalab yoki abetdan keyin telefon qilish kerak. Doniyor aka aytgandilar CRM linkini tashlab yuborsangiz yoki nimalar bo'lishi kerakligini aytsangiz biz sizga mos CRM tizimini taklif qilamiz\n\nrahbarim kelsin degandi\nqayta aloqaga chiqish kerak\n\n55 5005115\ninstagramdan topildi. tg sayt yo'q\n	cancel	4
18	Bayer Mineral water Muhammadjon	+998951638090	Ofisga borib lakatsiya tashlab qo'yaman dedi\nTelegiram bot yo'q. Web sayt yo'q. 	in_progres	4
151	Alyaska water 2	973358111	Telegramdan yozishganmiz\n	cancel	4
153	Elbrus	956052222	Navarasi aytishnik ekan Sayt bor bot yo'q	cancel	4
169	GROT WATER	901759731	Rahmat hozir kerak emas deyapti\nX	cancel	4
150	Alyaska water	781138989	nommerimizni yozib oldi o'zi aloqaga chiqar ekan\n\nnstagiram bor\nWeb sayt yo'q\nTelegiram bot yo'q	cancel	4
165	Mill water O'lmas	97 441 94 99	Telegramdan yozib qo'ying dedi\n\nchorshanba(21.05) yoki payshanba(22.05) telefon qilib lakatsiyasini so'rash kerak.\nkompaniya haqida ma'lumot berdim bu haftamas keyingi hafta gaplashaylik dedi\n\nErtaga telefon qilish kerak 14.05\n\nErtaga yoki indinga telefon qilish kerak\n5 daqiqa vaqtingiz bormi desam "To'g'risi ummuman vaqtim yo'q" dedi\nqachon telefon qilay bo'lmasa desam ertaga yoki indinga telefon qiling dedi\nX	in_progres	4
167	MEGA WATER COMPANY	(71) 255-49-45	TK\nTK\nTK\nTK\nTelefonni ko'tarmadi\nX	in_progres	4
162	Bulvar water	908661111	904436666 shu nommerga telefon qilib dardini eshitish kerak\n\nKeyinroq telefon qilar ekan.\nOldin CRM tizimini ishlatgan ekan. omoCRM ishlatgan ekan. CRM ishlatganimdan afsuslanyapman menga kerak emas ekan deyapti.\nX	cancel	4
173	Ma'ruf Miracle water	977993039	15.06 dan keyin tel qilish kerak\n\nBu suv yopilgan ekan. telegramdan yozish kerak lakatsiya so'rab. hozir balon sotish bilan shug'ullanishar ekan\n\n\nX	cancel	4
159	Safis water	781473113	Hammasi bor	empty	4
172	LION WATER	993097373	X	cancel	4
157	Azizbek Yaxtan water	993348950	CRM tizimi bor ekan. sotuvchilar uchun alohida kuryerlar uchun alohida CRM qildirgan ekan.\n\nTelefonni ko'tarmadi\n\n993348950-Azizbek \ntelefon raqami operatoridan olingan. bu rahbari ekan tel qilib xizmatlarimizni taklif qilish kerak\n\nBoshqa yo'nalishga javob beryapti\n\nTelefonni ko'tarmadi X	cancel	4
161	Uzbegimwater	950878000	Telegramdan tallif joʻnatib qoʻydim\n\ntelegramdan teklifni yozma ravishta jo'natish kerak\nX	cancel	4
200	Endlesswater	783330808	Suv ishlab chiqaradi. Instagiram faol telegiram bot bor\n	empty	4
201	Buloq suv	978994444	Suv ishlab chiqaradi instagiram bor	empty	4
208	Aquawater	901000066	Bot bor sayt yo'q\n	empty	4
108	Doniyor Brilliant Pure water	909097171	gaplashdim narigi nommeriga telefon qilish kerak.3113\n\nErtaga telefon qilish kerak. eski crm tizimi bor ekan shuni ko'rish uchun telefon qilish kerak. ko'rib chiqib qanday kamchiliklari bor biz bunga qanday yechim qilib bera olamiz\nBrilliant Pure water	cancel	1
187	Anjum water	888705225	Buxoda da joylashgan.\nOlx dan oldim	in_progres	4
109	Dawylife water Feruz	948789999	Sherigim kelsin maslahatlashib ko'ray degandi. botni narxini 100$ dan qilib bera olarkanmiz deyish kerak\n\nbir hatalarda tel qilish kerak 18.04\n\nHozir rasxot qilmay turay potent xal bo'lsin deyapti.\n\ntelegram botni o'ylab ko'ryapti\n\nSoft water bilan sherik ekan. ertaga ofisga kelishi kerak	in_progres	4
186	Temiz water	555208080	Ikkinchi raqam: 95 020 80 80\nInstagiramdan oldim	empty	3
188	Saxovat suvlari	997362020	Buxoroda joylashgan olxdan oldim	empty	4
189	Aqua Delux	971236663	Ikkinchi raqam: 93 140 88 83\nBuxoroda joylashgan\nOlxdan oldim	empty	4
191	Yasmin water	771070074	Buxoroda joylashgan olxdan oldim	empty	4
175	Aqualime Ibrohim	950635727	TK\nTK TK\nRulda edim dedi keyinroq tel qilish kerak\nTK\nSuv ishlab chiqazadu olx dan oldim\nIkkinchi raqami 992280504	in_progres	4
193	Murodbaxshsuv	555005070	Instagiramdan oldim	empty	4
163	Nest water	959543302	Azamat 18:00 dan keyin tel qilish kerak. Bu bo'yicha rahbarim bilan gaplashib ko'ray anig'ini aytaman dedi\nX	cancel	4
171	LIFE WATER	33 066 66 26	Raqami noto'g'ri X	empty	4
203	Elsuv	555180505	Suv ishlab chiqaradi instagiram aktiv boti bor web sayti ham bor tildada qilingan	empty	4
168	VODA KRISTALNAYA	(78) 140-02-51	Telegramdan yozib bo'lmadi sms ham ketmadi\nRus ekan o'zbekchani tushunmas ekan\nX	empty	4
196	Besh og'ayni milliy toamlari	909740070	2 Restaran\nChorsu gumda joylashgan	empty	4
198	Rayxon milliy taomlari	+998783332875	4- Reataran instagiram profili bor\nSamarqand darvada joylashgan	empty	4
12	Magicwater_uz	+998712036767	Kompaniya telefon raqamini managerlarga berib qo'yar ekan bizga o'zi aloqaga chiqadi\n\nTelegiram bot bor. Web sayti yo'q. \n	cancel	4
116	DR water	950410909	keyingi hafta yena bir telefon qilib habar olish kerak. telefon qilganda nima bo'ldi ishlarizni hal qildizmi deb so'rash kerak. (Nimadir hal bo'lsin o'zimiz aloqaga chiqamiz degan edi.) (23.05 da tel qilish kerak)\n\nTelefonni ko'tarmadi\n\nTelefonni ko'tarmasi\ntelefon qilganda qachon vaqti bor ko'risha olamizmi so'rash kerak\n\n\nTelefonni ko'tarmadi\n\n11.04 telefon qilish kerak\n\nTelefonni ko'tarmadi\n\nJurat. 09.04 ertaga ertalab telefon qilish kerak\n\nSayt bor, bot yo'q	in_progres	4
164	Fosso	950118228	Telegramdan ma'lumot tashlab qo'ydim\n974144197-Alibek\n\nTelefonni ko'tarmadi\n\nX	in_progres	4
204	tibet water	998745210	warter	cancel	4
205	Zarkent suv	990851505	Instagiram bor\nko'chada dastavka mashinasini ko'rib yozib oldim	empty	4
130	Zinnur pure	996066333	Iyul oyida qayta aloqaga chiqish kerak. Hozirda o'zini yani zavodni rivojlantirish bilan shug'ullanayotgan ekan bozorga chiqishga marketingga keyinroq harakat qilar ekan. sezon boshlangan lekin biz boshlay olmayapmiz dedi.\n\n976336333-Ziyovuddin Telefonni ko'tarmadi\n\nTelefonni ko'tarmadi\nTelefonni ko'tarmadi\nTelefonni ko'tarmadi\n\nXech nimasi yo'q	cancel	4
178	Shaffof Servis QK	71 278 00 88	Boshqa nommer ekan\nChatgpt dan oldim	cancel	4
199	Gumus su Jamshid	998429949	Bir soatdan keyin tel qilish kerak ekan 16:30\n\nSayti yo'q bot bor lekin ishlamayapti\n	in_progres	4
194	Aquazamin	991232228	Manageriga raqamimizni berib qo'yar ekan\nIkkinchi raqam: 1232229\nInstagiramdan oldim	cancel	4
206	Avera water 	555208048	Instagirami bor ikkinchi nomi divozamzam	empty	4
207	Nefrit suvlari	712093332	Suv ishlab chiqaradi instagiram mi telegiram boti bor	empty	4
121	Nafis suv  Abdullo	946693883	Telefonni o'chirib qo'ydi\nTelefonni koʻtarmadi\n\nTelefonni ko'tarmadi\nYangi O'zbekiston tomonda joylashgan\n\n10.04 soat 18:00 19:00 larda qayta aloqaga chiqish kerak\nqachon ko'rishsa bo'ladi so'rash kerak\nyangi o'zbekiston tomonda ekan\n\nAbdullo - 946693883\nDiyora - 947635070\nraqamini operatoridan olindi\nBot sayt yo'q\n	in_progres	4
183	Shaffof water	712008888	Yoʻq rahmat deb telefonni oʻchirib qoʻydi 909151122 - Shavkat \n\nInstagiramdan oldim. Veb sayt oldin bo'lgan hozir ishlamayapti.	cancel	4
181	Uz Aqua	71 201 11 22	Mavjud bo'lmagan raqam deyapti\nChatgpt dan oldim suv ishlab chiqadi	empty	4
180	Imir Trade Group	71 244 56 78	TK\nSuv ishlab chiqazadi\nWeb sayti bor lekin ishlamayapti	in_progres	4
182	Baraka Suvi	71 256 77 88	Sistemada mavjud emas deyapti\nChatgptda sergilida joylashgan dib ko'rsatdi.\nOlx da navoiyda dib ko'rsatdi raqami bitta	empty	4
202	Oqtosh meneral	771681111	Sayti bor bot yo'q\nBostoqliqda joylashgan suv ishlab chiqaradi. Instagirami bor	empty	4
190	Ewo water	330200520	Manga umuman kerak emas hozi boshqa ishlarim bor deyapti\n\nIkkinchi raqam: 33 007 37 27\nOlxdan oldim	cancel	4
192	La Vita water	951705858	Operatori oldi rahbarimizga telefon raqamingizni berib qo'yamiz dedi telegramdan yozib ham qo'ydim\n\nIkkinchi raqam: 71 203 58 58\nInstagiramdan oldim	in_progres	4
13	Minera life	+998908226644	Telefonni ko'tarmadi telegramdan yozsangiz tashlab beraman degani uchun telegramdan yozib qo'ydim\n\nKEchga soat 21:00 da telefon qilib meetga chaqirish kerak\n\nDushanba kechga meet qilib gaplashib olamiz\nErtaga (05.04.2025) ertalabdan abetgacha bo'lgan vaqt oralig'ida uchrashuv\nTelegiram bot bor lekin ishlamidi. Web sayti bor. Ofisiga bordik tapa olmadik.	cancel	4
195	Sayfullo shashlik	+998933841809	1 - Restaran\nNushafshon ko'chada joylashgan	in_progres	4
197	Kamolon Osh markazi	+998712455087	3- Restaran	in_progres	4
185	Begzod Tibet water	977751144	Borib gaplashib keldim korxonani  bsohqaruvchi CRM tizimi kerak ekan\n\nShanba kuni telefon qilib uchrashuv belgilash kerak\n\n\nPayshanba 15.05 kuni telegramdan yozish kerak vaqtiga qarab nechchida bo'sh bo'lishini aytadi va lakatsiya tashlab beradi\n\nBir joyga kirib ketayotgan ekan 1 soatlardan telefon qilish kerak\n\nSub ishlab chiqaradi. Instagiramdan oldim.	cancel	4
179	Blue Spring	71 235 67 89	Raqam sistemada mavjud emas deyapti\n\nTelefon raqam tarmoqda mavjud emas\nChatgpt dan oldim suv ishlab chiqadigan komponiya\n	empty	4
184	Just water	97 138 20 00	971382000 Shu raqamga telegramdan ma’lumot joʻnatish kerak\n\nSayt bor bot yo'q\n	in_progres	4
176	NEO suvlari	337715080	Kompaniya haqida ma'lumot berdim CRM ni narxini so'radi narxni aytdim yo'q bizga kerak emas ekan dedi. bispro CRM ishlatar ekan oyiga 350 ming to'layman dedi. 1 2 ta savol berganimdan keyin o'zim telefon qilsam bo'ladimi dedi\n\nTK\nSuv ishlab chiqadi Olx dan oldim	in_progres	4
174	Geolife	941479000	Maslahatlashib ko'raman dedi\n\nTK TK\nKeyinroq tell qilish kerak 18:00\n\n21.05 Telegramdan ma'lumot tashlab qo'ydim ertaga yena telefon qilib Nima bo'ldi ko'rib chiqdingizmi vaqtingiz bo'lsa biron kun belgilab ko'rishib olsak batafsil ma'lumot berib kelar edim deyish kerak\nX	cancel	4
209	O'quv markaz Dilbar	881160917	Nurafshon tomonda ekan\n\nSardor SMM xizmati bo'yicha yozgan ekan	empty	1
210	Bot. Xisobchi bot	500307624	Xisobchi botga oʻxshagan bot soʻragandi 2 3 haftadan keyin xabar olish kerak tahminan 25.07	empty	1
211	minimdesign.uz	+998 97 400-04-13	Sayti yonib yotibdi\n	empty	4
\.


--
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.positions (id, name) FROM stdin;
1	Rahbar
2	Backend dasturchi
3	Frontend dasturchi
4	Flutter dasturchi
5	SMM manager
6	Designer
7	Project Manager
8	Farrosh
9	Bugalter
\.


--
-- Data for Name: project_programmer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_programmer (id, project_id, programmer_id) FROM stdin;
226	31	7
227	31	6
228	31	8
115	10	6
116	10	11
235	6	5
236	6	3
237	6	6
238	32	3
239	32	22
240	32	6
241	32	12
242	32	9
243	32	11
244	33	9
245	33	19
246	34	8
247	35	9
248	35	11
182	7	7
183	7	6
184	7	11
185	7	3
122	8	3
123	8	8
124	8	11
249	35	8
250	36	8
251	37	11
252	37	16
253	38	11
254	38	16
51	11	6
52	12	7
99	9	7
100	9	6
101	9	11
102	9	3
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, name, start_date, end_date, status, image, price, is_deleted) FROM stdin;
6	WTC	2025-01-31 00:00:00	2025-02-13 00:00:00	done	project/None	15600000	f
32	Chimgan water	2025-04-22 00:00:00	2025-05-10 00:00:00	in_progres	projects/None	12900000	f
7	One PC	2024-11-01 00:00:00	2025-02-20 00:00:00	done	project/None	9100000	f
9	Motostan	2024-12-10 00:00:00	2025-02-15 00:00:00	done	project/None	1300000	f
8	OGMK CRM	2024-12-15 00:00:00	2025-02-05 00:00:00	done	project/None	23500000	f
34	Mauntain Ceo hizmati	2025-05-08 00:00:00	2025-08-08 00:00:00	in_progres	projects/None	7800000	f
36	Aroma atir	2025-05-15 00:00:00	2025-06-15 00:00:00	in_progres	projects/None	2600000	f
37	Crestal Ice Smm	2025-07-17 00:00:00	2025-09-17 00:00:00	in_progres	projects/None	12700000	f
38	Neosocial seo	2025-08-20 00:00:00	2025-11-20 00:00:00	in_progres	projects/None	2600000	f
33	Canfort Smm hizmati	2025-05-01 00:00:00	2025-05-31 00:00:00	done	projects/None	5200000	f
35	Azim Studio	2025-05-15 00:00:00	2025-05-31 00:00:00	done	projects/None	3900000	f
12	Marwa tour ( Kartaga ulab berish)	2025-01-15 00:00:00	2025-01-16 00:00:00	done	projects/None	300000	f
11	Fayz to'yxona ( forma )	2025-01-15 00:00:00	2025-01-16 00:00:00	done	projects/None	300000	f
10	Media zone ( Sevi.lv )	2025-02-04 00:00:00	2025-02-05 00:00:00	done	project/None	1300000	f
31	agency sayt	2025-03-26 00:00:00	2025-03-31 00:00:00	done	projects/None	6000000	f
\.


--
-- Data for Name: task_programmer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_programmer (id, task_id, programmer_id) FROM stdin;
1	1	4
2	1	8
3	2	4
4	2	8
5	3	4
6	3	7
12	4	8
13	4	7
14	4	5
18	6	4
19	6	7
20	6	6
35	5	4
36	5	7
37	5	6
38	7	4
39	7	7
40	8	4
41	8	3
42	9	4
43	10	3
44	10	4
45	11	4
46	11	3
47	11	8
48	12	3
49	12	4
50	13	4
51	14	3
52	15	4
53	16	3
54	16	14
55	16	15
56	17	4
57	18	7
58	19	20
59	19	7
60	19	6
63	20	6
64	20	7
69	21	6
70	21	7
71	22	3
72	22	20
73	23	20
74	23	3
75	24	7
76	25	7
77	25	6
78	26	14
81	29	15
82	28	3
83	30	3
84	31	6
85	32	8
94	34	7
95	35	4
97	36	20
98	37	7
99	38	7
100	39	6
101	40	6
102	27	4
103	41	4
104	42	20
105	43	4
106	43	20
108	44	6
109	45	4
114	46	3
115	46	8
116	47	15
117	47	8
118	47	22
119	33	7
120	33	8
121	33	3
122	33	20
123	48	22
124	48	15
125	48	8
126	49	8
127	49	22
128	50	15
129	50	8
130	51	5
131	51	22
132	52	3
133	52	15
134	53	3
135	54	20
136	54	7
137	54	6
138	55	8
139	55	3
140	56	28
141	57	3
142	57	15
143	57	6
144	58	28
145	59	28
146	60	28
147	61	15
148	62	15
149	63	6
150	64	28
151	65	28
152	66	28
153	67	30
154	68	30
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, name, start_date, end_date, status, is_deleted, description, image_task) FROM stdin;
36	front-end	2025-02-01 00:00:00	2025-02-26 00:00:00	to_do	t	iuerbgeiu ger	20210617_010331.jpg
37	2front-end	2025-02-01 00:00:00	2025-02-26 00:00:00	to_do	t	gnierbg gerjgb	\N
18	Frontend	2025-02-01 00:00:00	2025-02-11 00:00:00	to_do	t	sefwe gegew gw	\N
9	Mavlon	2025-02-07 00:00:00	2025-02-07 00:00:00	to_do	t	gerge gerge	\N
1	asdasd	2025-02-03 00:00:00	2025-02-06 00:00:00	in_progres	t	asdas	\N
2	asdasd	2025-01-28 00:00:00	2025-02-12 00:00:00	to_do	t	asdasd	\N
3	asdasd	2025-01-28 00:00:00	2025-02-19 00:00:00	to_do	t	asdasd	\N
6	CRM vazifalar	2025-02-07 00:00:00	2025-02-10 00:00:00	to_do	t	Vazifalarni faqat hammasini rahbar koraolsin qolgan vazifalar kimga tegishli bolsa shular ham korin. Agar hamma koradigan bolsa mujmal bolib ketadi	\N
4	asdas	2025-01-27 00:00:00	2025-02-04 00:00:00	to_do	t	dffdfghdf	\N
19	backend	2025-02-03 00:00:00	2025-02-17 00:00:00	in_progres	t	fieuwbf fewiuf	image.png
8	KattaPul	2025-02-07 00:00:00	2025-02-07 00:00:00	to_do	t	sdfsdfsdfsdfsdf	\N
10	fhewfe	2025-02-08 00:00:00	2025-02-08 00:00:00	to_do	t	g3ger gerg	\N
11	fe3rge rege	2025-02-01 00:00:00	2025-02-08 00:00:00	in_progres	t	erger erger erg	\N
17	Pul topish 	2025-02-15 00:00:00	2025-02-18 00:00:00	to_do	t	Koproq pul topish	\N
20	Backend	2025-02-04 00:00:00	2025-02-17 00:00:00	in_progres	t	fwef werw	fir df.png
12	sfds	2025-02-01 00:00:00	2025-02-09 00:00:00	to_do	t	sdfsd	\N
7	hjhk	2025-02-13 00:00:00	2025-02-04 00:00:00	to_do	t	jhgjhg	\N
5	CRM chat	2025-02-06 00:00:00	2025-02-13 00:00:00	code_review	t	Ikkinchi versiyada qilinadi chat bajarish kerak	\N
39	2front-end	2025-02-26 00:00:00	2025-02-27 00:00:00	to_do	t	gbierubg gerbgi	20210617_010331.jpg
38	front-end	2025-02-01 00:00:00	2025-02-26 00:00:00	to_do	t	fheiug teriutb	20210617_010331.jpg
40	front-end2	2025-02-01 00:00:00	2025-02-26 00:00:00	to_do	t	fieurbgie geiurbg	\N
13	Test	2025-02-10 00:00:00	2025-02-11 00:00:00	to_do	t	Test	\N
24	Backend	2025-02-01 00:00:00	2025-02-17 00:00:00	in_progres	t	beiurbg	image.png
22	Backend	2025-02-01 00:00:00	2025-02-17 00:00:00	code_review	t	WTC\r\n	fir df.png
23	Backend	2025-02-01 00:00:00	2025-02-17 00:00:00	code_review	t	fwe	fir df.png
21	front end	2025-02-01 00:00:00	2025-02-17 00:00:00	done	t	Moy 	ae8ac2fa217d23aadcc913989fcc34a2.png
16	Backend	2025-02-13 00:00:00	2025-02-11 00:00:00	success	t	gerg erger	\N
25	front end	2025-02-01 00:00:00	2025-02-17 00:00:00	in_progres	t	fewg erge	image.png
27	navbarni to'g'irlash kerak	2025-02-21 00:00:00	2025-02-28 00:00:00	code_review	t	undefined	20210617_010331.jpg
26	string	2025-02-20 00:00:00	2025-02-20 00:00:00	code_review	t	string	\N
54	qwert	2025-03-01 00:00:00	2025-03-31 00:00:00	success	f	undefined\r\n	\N
50	qwertyu	2025-03-31 00:00:00	2025-04-03 00:00:00	to_do	t	qwertyu	\N
42	front-end	2025-03-03 00:00:00	2025-03-31 00:00:00	in_progres	t	teriutebr gberuibgeui	3d_sphere-1920x1080.jpg
14	complite wtc backend 	2025-02-10 00:00:00	2025-02-12 00:00:00	to_do	t	new task	\N
51	qwertyu	2025-03-22 00:00:00	2025-03-31 00:00:00	to_do	t	qwertg	\N
15	sdxsd	2025-02-12 00:00:00	2025-02-12 00:00:00	success	t	asdasdasd	\N
41	front-end	2025-03-03 00:00:00	2025-03-05 00:00:00	to_do	t	gebirubgei geriubgeiug	art_game_scene.jpg
31	WTC ni textlarini to'g'irlash kerak	2025-02-11 00:00:00	2025-02-15 00:00:00	success	t	undefined	\N
28	WTC ni kamchiliklarini to'g'irlash kerak	2025-02-01 00:00:00	2025-02-25 00:00:00	done	t	undefined	\N
29	WTC ga kontent qo'shib chiqish kerak	2025-02-21 00:00:00	2025-02-25 00:00:00	done	t	undefined	\N
52	qwerty	2025-03-01 00:00:00	2025-03-03 00:00:00	to_do	t	qwert	\N
30	WTC ni kontentlarini qo'shish kerak	2025-02-10 00:00:00	2025-02-15 00:00:00	success	f	undefined	\N
44	sdfg	2025-03-01 00:00:00	2025-03-04 00:00:00	to_do	t	sdfg	IMG_5524.jpg
65	test	2025-05-28 00:00:00	2025-05-29 00:00:00	code_review	t	1231234	\N
35	front-end	2025-02-01 00:00:00	2025-02-26 00:00:00	to_do	t	geiurbge	20210617_010331.jpg
34	front-end	2025-02-01 00:00:00	2025-02-26 00:00:00	to_do	t	ngeiurb	20210617_010331.jpg
43	...	2025-03-01 00:00:00	2025-03-04 00:00:00	to_do	t	erty	Artboard 1 copy@3x.png
45	Katta pul topish	2025-03-04 00:00:00	2025-03-31 00:00:00	to_do	t	katata	photo_2024-10-30_18-56-34.jpg
66	test	2025-05-28 00:00:00	2025-05-30 00:00:00	to_do	t	test	\N
46	qwert	2025-03-01 00:00:00	2025-03-04 00:00:00	to_do	t	qwert	512px-Map_of_Central_Asia.svg.png
47	qqwert	2025-03-01 00:00:00	2025-03-18 00:00:00	to_do	t	qwewtre	Professional Photo.jpeg
33	WTC ni test qilish kerak	2025-02-13 00:00:00	2025-02-15 00:00:00	done	t	undefined	\N
48	qwert	2025-03-01 00:00:00	2025-03-18 00:00:00	done	t	qwert	STP-Produkte-Auto-013.webp
49	qwert	2025-03-01 00:00:00	2025-03-04 00:00:00	to_do	t	1234qwer	\N
58	test	2025-05-27 00:00:00	2025-05-29 00:00:00	to_do	t	1234	\N
55	Brendlar boʻyicha saralash kerak	2025-05-03 00:00:00	2025-05-04 00:00:00	to_do	f	undefined	\N
57	fsfd	2025-05-17 00:00:00	2025-05-24 00:00:00	to_do	f	asdff	\N
63	wewewe	2025-05-27 00:00:00	2025-05-28 00:00:00	in_progres	f	testt	\N
53	CRM tasklarni	2025-03-22 00:00:00	2025-03-31 00:00:00	in_progres	f	undefined	\N
59	test	2025-05-28 00:00:00	2025-05-30 00:00:00	done	t	134124	\N
32	Footerni to'g'irlash kerak	2025-02-13 00:00:00	2025-02-15 00:00:00	success	f	undefined	\N
56	test	2025-05-09 00:00:00	2025-05-10 00:00:00	code_review	t	test	\N
60	test	2025-05-27 00:00:00	2025-05-30 00:00:00	code_review	t	testttt	\N
61	wewewe	2025-05-28 00:00:00	2025-05-31 00:00:00	success	f	шгнек	\N
64	wewewe	2025-05-22 00:00:00	2025-05-30 00:00:00	done	t	1313123	\N
62	test223	2025-05-28 00:00:00	2025-05-31 00:00:00	done	f	testttt	\N
68	deded	2025-08-12 00:00:00	2025-08-19 00:00:00	success	t	deded	\N
67	ee	2025-08-14 00:00:00	2025-08-11 00:00:00	success	t	ded	\N
\.


--
-- Name: chat_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_room_id_seq', 4, true);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 33, true);


--
-- Name: expected_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.expected_value_id_seq', 29, true);


--
-- Name: expences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.expences_id_seq', 365, true);


--
-- Name: incomes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.incomes_id_seq', 112, true);


--
-- Name: login_pass_note_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_pass_note_id_seq', 14, true);


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.message_id_seq', 112, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- Name: operator_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.operator_type_id_seq', 4, true);


--
-- Name: operators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.operators_id_seq', 211, true);


--
-- Name: positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.positions_id_seq', 9, true);


--
-- Name: project_programmer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_programmer_id_seq', 254, true);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 38, true);


--
-- Name: task_programmer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_programmer_id_seq', 154, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 68, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: chat_room chat_room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_room
    ADD CONSTRAINT chat_room_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: employees employees_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_username_key UNIQUE (username);


--
-- Name: expected_value expected_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expected_value
    ADD CONSTRAINT expected_value_pkey PRIMARY KEY (id);


--
-- Name: expences expences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expences
    ADD CONSTRAINT expences_pkey PRIMARY KEY (id);


--
-- Name: incomes incomes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incomes
    ADD CONSTRAINT incomes_pkey PRIMARY KEY (id);


--
-- Name: login_pass_note login_pass_note_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login_pass_note
    ADD CONSTRAINT login_pass_note_pkey PRIMARY KEY (id);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: operator_type operator_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operator_type
    ADD CONSTRAINT operator_type_pkey PRIMARY KEY (id);


--
-- Name: operators operators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operators
    ADD CONSTRAINT operators_pkey PRIMARY KEY (id);


--
-- Name: positions positions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (id);


--
-- Name: project_programmer project_programmer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_programmer
    ADD CONSTRAINT project_programmer_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: task_programmer task_programmer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_programmer
    ADD CONSTRAINT task_programmer_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: ix_employees_image; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_employees_image ON public.employees USING btree (image);


--
-- Name: ix_projects_image; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_projects_image ON public.projects USING btree (image);


--
-- Name: chat_room chat_room_user1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_room
    ADD CONSTRAINT chat_room_user1_id_fkey FOREIGN KEY (user1_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: chat_room chat_room_user2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_room
    ADD CONSTRAINT chat_room_user2_id_fkey FOREIGN KEY (user2_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: employees employees_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.positions(id) ON DELETE CASCADE;


--
-- Name: expences expences_employee_salary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expences
    ADD CONSTRAINT expences_employee_salary_id_fkey FOREIGN KEY (employee_salary_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: incomes incomes_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incomes
    ADD CONSTRAINT incomes_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: message message_chat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES public.chat_room(id) ON DELETE CASCADE;


--
-- Name: message message_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: operators operators_operator_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operators
    ADD CONSTRAINT operators_operator_type_id_fkey FOREIGN KEY (operator_type_id) REFERENCES public.operator_type(id) ON DELETE CASCADE;


--
-- Name: project_programmer project_programmer_programmer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_programmer
    ADD CONSTRAINT project_programmer_programmer_id_fkey FOREIGN KEY (programmer_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: project_programmer project_programmer_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_programmer
    ADD CONSTRAINT project_programmer_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: task_programmer task_programmer_programmer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_programmer
    ADD CONSTRAINT task_programmer_programmer_id_fkey FOREIGN KEY (programmer_id) REFERENCES public.employees(id);


--
-- Name: task_programmer task_programmer_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_programmer
    ADD CONSTRAINT task_programmer_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- PostgreSQL database dump complete
--

