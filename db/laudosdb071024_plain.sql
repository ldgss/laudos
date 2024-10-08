--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-10-07 02:02:33

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
-- TOC entry 216 (class 1259 OID 16722)
-- Name: acceso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acceso (
    id bigint NOT NULL,
    ip text NOT NULL,
    dispositvo text NOT NULL,
    usuario bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.acceso OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16721)
-- Name: acceso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.acceso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.acceso_id_seq OWNER TO postgres;

--
-- TOC entry 4933 (class 0 OID 0)
-- Dependencies: 215
-- Name: acceso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.acceso_id_seq OWNED BY public.acceso.id;


--
-- TOC entry 218 (class 1259 OID 16731)
-- Name: bloqueado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bloqueado (
    id bigint NOT NULL,
    mercaderia bigint,
    hojalata bigint,
    extracto bigint,
    estado boolean NOT NULL,
    numero_planilla text NOT NULL,
    motivo bigint NOT NULL,
    observaciones text,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.bloqueado OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16730)
-- Name: bloqueado_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bloqueado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bloqueado_id_seq OWNER TO postgres;

--
-- TOC entry 4934 (class 0 OID 0)
-- Dependencies: 217
-- Name: bloqueado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bloqueado_id_seq OWNED BY public.bloqueado.id;


--
-- TOC entry 220 (class 1259 OID 16740)
-- Name: despacho; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.despacho (
    id bigint NOT NULL,
    mercaderia bigint,
    hojalata bigint,
    extracto bigint,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    orden_entrega bigint
);


ALTER TABLE public.despacho OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16739)
-- Name: despacho_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.despacho_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.despacho_id_seq OWNER TO postgres;

--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 219
-- Name: despacho_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.despacho_id_seq OWNED BY public.despacho.id;


--
-- TOC entry 222 (class 1259 OID 16747)
-- Name: extracto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extracto (
    id bigint NOT NULL,
    numero_unico text NOT NULL,
    productro bigint NOT NULL,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    recipiente text NOT NULL,
    numero_recipiente bigint NOT NULL,
    observaciones text,
    vto_meses bigint NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.extracto OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16746)
-- Name: extracto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.extracto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.extracto_id_seq OWNER TO postgres;

--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 221
-- Name: extracto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.extracto_id_seq OWNED BY public.extracto.id;


--
-- TOC entry 226 (class 1259 OID 16765)
-- Name: hojalata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hojalata (
    id bigint NOT NULL,
    producto bigint NOT NULL,
    observacion text,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    lote_cuerpo text,
    lote_tapa text,
    cantidad bigint NOT NULL,
    numero_unico text NOT NULL,
    responsable bigint NOT NULL,
    vto_meses bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.hojalata OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16764)
-- Name: hojalata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hojalata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hojalata_id_seq OWNER TO postgres;

--
-- TOC entry 4937 (class 0 OID 0)
-- Dependencies: 225
-- Name: hojalata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hojalata_id_seq OWNED BY public.hojalata.id;


--
-- TOC entry 224 (class 1259 OID 16756)
-- Name: insumo_envase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insumo_envase (
    id bigint NOT NULL,
    producto bigint NOT NULL,
    numero_unico text NOT NULL,
    fecha_consumo timestamp with time zone NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.insumo_envase OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16755)
-- Name: insumo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.insumo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.insumo_id_seq OWNER TO postgres;

--
-- TOC entry 4938 (class 0 OID 0)
-- Dependencies: 223
-- Name: insumo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.insumo_id_seq OWNED BY public.insumo_envase.id;


--
-- TOC entry 228 (class 1259 OID 16774)
-- Name: mercaderia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mercaderia (
    id bigint NOT NULL,
    producto bigint NOT NULL,
    observacion text,
    cantidad bigint NOT NULL,
    lote text NOT NULL,
    fecha_elaboracion timestamp with time zone,
    fecha_etiquetado timestamp with time zone,
    responsable bigint NOT NULL,
    numero_unico text NOT NULL,
    vto_meses bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    antecedentes text,
    fecha_encajonado timestamp with time zone
);


ALTER TABLE public.mercaderia OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16773)
-- Name: mercaderia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mercaderia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mercaderia_id_seq OWNER TO postgres;

--
-- TOC entry 4939 (class 0 OID 0)
-- Dependencies: 227
-- Name: mercaderia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mercaderia_id_seq OWNED BY public.mercaderia.id;


--
-- TOC entry 230 (class 1259 OID 16783)
-- Name: motivo_bloqueo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.motivo_bloqueo (
    id bigint NOT NULL,
    motivo text NOT NULL,
    mercaderia boolean NOT NULL,
    hojalata boolean NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    extracto boolean NOT NULL
);


ALTER TABLE public.motivo_bloqueo OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16782)
-- Name: motivo_bloqueo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.motivo_bloqueo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.motivo_bloqueo_id_seq OWNER TO postgres;

--
-- TOC entry 4940 (class 0 OID 0)
-- Dependencies: 229
-- Name: motivo_bloqueo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.motivo_bloqueo_id_seq OWNED BY public.motivo_bloqueo.id;


--
-- TOC entry 232 (class 1259 OID 16792)
-- Name: permiso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permiso (
    id bigint NOT NULL,
    mercaderia boolean NOT NULL,
    hojalata boolean NOT NULL,
    ubicacion boolean NOT NULL,
    bloqueo boolean NOT NULL,
    usuario boolean NOT NULL,
    despacho boolean NOT NULL,
    insumo boolean NOT NULL,
    extracto boolean NOT NULL,
    acceso boolean NOT NULL,
    motivo_bloqueo boolean NOT NULL,
    permiso boolean NOT NULL,
    vencimiento boolean NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.permiso OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16791)
-- Name: permiso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permiso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permiso_id_seq OWNER TO postgres;

--
-- TOC entry 4941 (class 0 OID 0)
-- Dependencies: 231
-- Name: permiso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permiso_id_seq OWNED BY public.permiso.id;


--
-- TOC entry 234 (class 1259 OID 16799)
-- Name: ubicacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicacion (
    id bigint NOT NULL,
    ubicacion bigint NOT NULL,
    mercaderia bigint,
    hojalata bigint,
    extracto bigint,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    alt_profundidad text,
    alt_altura text,
    insumo_envase bigint
);


ALTER TABLE public.ubicacion OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16798)
-- Name: ubicacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ubicacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ubicacion_id_seq OWNER TO postgres;

--
-- TOC entry 4942 (class 0 OID 0)
-- Dependencies: 233
-- Name: ubicacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicacion_id_seq OWNED BY public.ubicacion.id;


--
-- TOC entry 240 (class 1259 OID 17172)
-- Name: ubicaciones_nombres; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicaciones_nombres (
    id bigint NOT NULL,
    posicion text NOT NULL,
    sector text NOT NULL
);


ALTER TABLE public.ubicaciones_nombres OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 17171)
-- Name: ubicaciones_nombres_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ubicaciones_nombres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ubicaciones_nombres_id_seq OWNER TO postgres;

--
-- TOC entry 4943 (class 0 OID 0)
-- Dependencies: 239
-- Name: ubicaciones_nombres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicaciones_nombres_id_seq OWNED BY public.ubicaciones_nombres.id;


--
-- TOC entry 236 (class 1259 OID 16806)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id bigint NOT NULL,
    nombre text NOT NULL,
    password text NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_modificacion timestamp with time zone NOT NULL,
    esta_activo boolean NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16805)
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_seq OWNER TO postgres;

--
-- TOC entry 4944 (class 0 OID 0)
-- Dependencies: 235
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- TOC entry 238 (class 1259 OID 16816)
-- Name: vencimiento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vencimiento (
    id bigint NOT NULL,
    producto bigint NOT NULL,
    meses bigint NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.vencimiento OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16815)
-- Name: vencimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vencimiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vencimiento_id_seq OWNER TO postgres;

--
-- TOC entry 4945 (class 0 OID 0)
-- Dependencies: 237
-- Name: vencimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vencimiento_id_seq OWNED BY public.vencimiento.id;


--
-- TOC entry 4694 (class 2604 OID 16725)
-- Name: acceso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso ALTER COLUMN id SET DEFAULT nextval('public.acceso_id_seq'::regclass);


--
-- TOC entry 4695 (class 2604 OID 16734)
-- Name: bloqueado id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado ALTER COLUMN id SET DEFAULT nextval('public.bloqueado_id_seq'::regclass);


--
-- TOC entry 4696 (class 2604 OID 16743)
-- Name: despacho id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho ALTER COLUMN id SET DEFAULT nextval('public.despacho_id_seq'::regclass);


--
-- TOC entry 4697 (class 2604 OID 16750)
-- Name: extracto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto ALTER COLUMN id SET DEFAULT nextval('public.extracto_id_seq'::regclass);


--
-- TOC entry 4699 (class 2604 OID 16768)
-- Name: hojalata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata ALTER COLUMN id SET DEFAULT nextval('public.hojalata_id_seq'::regclass);


--
-- TOC entry 4698 (class 2604 OID 16759)
-- Name: insumo_envase id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase ALTER COLUMN id SET DEFAULT nextval('public.insumo_id_seq'::regclass);


--
-- TOC entry 4700 (class 2604 OID 16777)
-- Name: mercaderia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia ALTER COLUMN id SET DEFAULT nextval('public.mercaderia_id_seq'::regclass);


--
-- TOC entry 4701 (class 2604 OID 16786)
-- Name: motivo_bloqueo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo ALTER COLUMN id SET DEFAULT nextval('public.motivo_bloqueo_id_seq'::regclass);


--
-- TOC entry 4702 (class 2604 OID 16795)
-- Name: permiso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso ALTER COLUMN id SET DEFAULT nextval('public.permiso_id_seq'::regclass);


--
-- TOC entry 4703 (class 2604 OID 16802)
-- Name: ubicacion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion ALTER COLUMN id SET DEFAULT nextval('public.ubicacion_id_seq'::regclass);


--
-- TOC entry 4706 (class 2604 OID 17175)
-- Name: ubicaciones_nombres id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones_nombres ALTER COLUMN id SET DEFAULT nextval('public.ubicaciones_nombres_id_seq'::regclass);


--
-- TOC entry 4704 (class 2604 OID 16809)
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- TOC entry 4705 (class 2604 OID 16819)
-- Name: vencimiento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento ALTER COLUMN id SET DEFAULT nextval('public.vencimiento_id_seq'::regclass);


--
-- TOC entry 4903 (class 0 OID 16722)
-- Dependencies: 216
-- Data for Name: acceso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.acceso (id, ip, dispositvo, usuario, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4905 (class 0 OID 16731)
-- Dependencies: 218
-- Data for Name: bloqueado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bloqueado (id, mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4907 (class 0 OID 16740)
-- Dependencies: 220
-- Data for Name: despacho; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.despacho (id, mercaderia, hojalata, extracto, responsable, fecha_registro, orden_entrega) FROM stdin;
\.


--
-- TOC entry 4909 (class 0 OID 16747)
-- Dependencies: 222
-- Data for Name: extracto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extracto (id, numero_unico, productro, fecha_elaboracion, lote, recipiente, numero_recipiente, observaciones, vto_meses, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4913 (class 0 OID 16765)
-- Dependencies: 226
-- Data for Name: hojalata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hojalata (id, producto, observacion, fecha_elaboracion, lote, lote_cuerpo, lote_tapa, cantidad, numero_unico, responsable, vto_meses, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4911 (class 0 OID 16756)
-- Dependencies: 224
-- Data for Name: insumo_envase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insumo_envase (id, producto, numero_unico, fecha_consumo, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4915 (class 0 OID 16774)
-- Dependencies: 228
-- Data for Name: mercaderia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderia (id, producto, observacion, cantidad, lote, fecha_elaboracion, fecha_etiquetado, responsable, numero_unico, vto_meses, fecha_registro, antecedentes, fecha_encajonado) FROM stdin;
\.


--
-- TOC entry 4917 (class 0 OID 16783)
-- Dependencies: 230
-- Data for Name: motivo_bloqueo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.motivo_bloqueo (id, motivo, mercaderia, hojalata, responsable, fecha_registro, extracto) FROM stdin;
\.


--
-- TOC entry 4919 (class 0 OID 16792)
-- Dependencies: 232
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permiso (id, mercaderia, hojalata, ubicacion, bloqueo, usuario, despacho, insumo, extracto, acceso, motivo_bloqueo, permiso, vencimiento, responsable, fecha_registro) FROM stdin;
1	t	f	t	t	t	t	t	f	t	t	t	t	1	2024-09-07 17:02:32.860241-03
\.


--
-- TOC entry 4921 (class 0 OID 16799)
-- Dependencies: 234
-- Data for Name: ubicacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicacion (id, ubicacion, mercaderia, hojalata, extracto, responsable, fecha_registro, alt_profundidad, alt_altura, insumo_envase) FROM stdin;
\.


--
-- TOC entry 4927 (class 0 OID 17172)
-- Dependencies: 240
-- Data for Name: ubicaciones_nombres; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicaciones_nombres (id, posicion, sector) FROM stdin;
\.


--
-- TOC entry 4923 (class 0 OID 16806)
-- Dependencies: 236
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id, nombre, password, fecha_creacion, fecha_modificacion, esta_activo) FROM stdin;
1	laureano	abc123	2024-09-07 15:20:02.852177-03	2024-09-07 15:20:02.852177-03	t
\.


--
-- TOC entry 4925 (class 0 OID 16816)
-- Dependencies: 238
-- Data for Name: vencimiento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vencimiento (id, producto, meses, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4946 (class 0 OID 0)
-- Dependencies: 215
-- Name: acceso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.acceso_id_seq', 1, false);


--
-- TOC entry 4947 (class 0 OID 0)
-- Dependencies: 217
-- Name: bloqueado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bloqueado_id_seq', 1, false);


--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 219
-- Name: despacho_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.despacho_id_seq', 1, false);


--
-- TOC entry 4949 (class 0 OID 0)
-- Dependencies: 221
-- Name: extracto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extracto_id_seq', 1, false);


--
-- TOC entry 4950 (class 0 OID 0)
-- Dependencies: 225
-- Name: hojalata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hojalata_id_seq', 1, false);


--
-- TOC entry 4951 (class 0 OID 0)
-- Dependencies: 223
-- Name: insumo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.insumo_id_seq', 1, false);


--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 227
-- Name: mercaderia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mercaderia_id_seq', 1, false);


--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 229
-- Name: motivo_bloqueo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.motivo_bloqueo_id_seq', 1, false);


--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 231
-- Name: permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permiso_id_seq', 1, true);


--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 233
-- Name: ubicacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicacion_id_seq', 1, false);


--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 239
-- Name: ubicaciones_nombres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicaciones_nombres_id_seq', 1, false);


--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 235
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_seq', 1, true);


--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 237
-- Name: vencimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vencimiento_id_seq', 1, false);


--
-- TOC entry 4708 (class 2606 OID 16729)
-- Name: acceso acceso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT acceso_pkey PRIMARY KEY (id);


--
-- TOC entry 4710 (class 2606 OID 16738)
-- Name: bloqueado bloqueado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT bloqueado_pkey PRIMARY KEY (id);


--
-- TOC entry 4712 (class 2606 OID 16745)
-- Name: despacho despacho_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT despacho_pkey PRIMARY KEY (id);


--
-- TOC entry 4714 (class 2606 OID 16754)
-- Name: extracto extracto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_pkey PRIMARY KEY (id);


--
-- TOC entry 4718 (class 2606 OID 16772)
-- Name: hojalata hojalata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT hojalata_pkey PRIMARY KEY (id);


--
-- TOC entry 4716 (class 2606 OID 16763)
-- Name: insumo_envase insumo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT insumo_pkey PRIMARY KEY (id);


--
-- TOC entry 4720 (class 2606 OID 16781)
-- Name: mercaderia mercaderia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT mercaderia_pkey PRIMARY KEY (id);


--
-- TOC entry 4722 (class 2606 OID 16790)
-- Name: motivo_bloqueo motivo_bloqueo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT motivo_bloqueo_pkey PRIMARY KEY (id);


--
-- TOC entry 4724 (class 2606 OID 16797)
-- Name: permiso permiso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT permiso_pkey PRIMARY KEY (id);


--
-- TOC entry 4726 (class 2606 OID 16804)
-- Name: ubicacion ubicacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT ubicacion_pkey PRIMARY KEY (id);


--
-- TOC entry 4732 (class 2606 OID 17177)
-- Name: ubicaciones_nombres ubicaciones_nombres_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones_nombres
    ADD CONSTRAINT ubicaciones_nombres_pkey PRIMARY KEY (id);


--
-- TOC entry 4728 (class 2606 OID 16813)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- TOC entry 4730 (class 2606 OID 16821)
-- Name: vencimiento vencimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT vencimiento_pkey PRIMARY KEY (id);


--
-- TOC entry 4733 (class 2606 OID 16828)
-- Name: acceso FK_acceso_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT "FK_acceso_usuario" FOREIGN KEY (usuario) REFERENCES public.usuario(id);


--
-- TOC entry 4734 (class 2606 OID 17047)
-- Name: bloqueado FK_bloqueado_extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);


--
-- TOC entry 4735 (class 2606 OID 17042)
-- Name: bloqueado FK_bloqueado_hojalata; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);


--
-- TOC entry 4736 (class 2606 OID 17037)
-- Name: bloqueado FK_bloqueado_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);


--
-- TOC entry 4737 (class 2606 OID 17032)
-- Name: bloqueado FK_bloqueado_motivo_bloqueo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_motivo_bloqueo" FOREIGN KEY (motivo) REFERENCES public.motivo_bloqueo(id);


--
-- TOC entry 4738 (class 2606 OID 17027)
-- Name: bloqueado FK_bloqueado_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4739 (class 2606 OID 17082)
-- Name: despacho FK_despacho_extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);


--
-- TOC entry 4740 (class 2606 OID 17077)
-- Name: despacho FK_despacho_hojalata; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);


--
-- TOC entry 4741 (class 2606 OID 17072)
-- Name: despacho FK_despacho_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);


--
-- TOC entry 4742 (class 2606 OID 17087)
-- Name: despacho FK_despacho_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4743 (class 2606 OID 16951)
-- Name: extracto FK_extracto_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "FK_extracto_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4744 (class 2606 OID 16946)
-- Name: extracto FK_extracto_vencimiento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "FK_extracto_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);


--
-- TOC entry 4746 (class 2606 OID 16917)
-- Name: hojalata FK_hojalata_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT "FK_hojalata_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4747 (class 2606 OID 16912)
-- Name: hojalata FK_hojalata_vencimiento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT "FK_hojalata_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);


--
-- TOC entry 4745 (class 2606 OID 16865)
-- Name: insumo_envase FK_insumo_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT "FK_insumo_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4748 (class 2606 OID 16974)
-- Name: mercaderia FK_mercaderia_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT "FK_mercaderia_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4749 (class 2606 OID 16991)
-- Name: mercaderia FK_mercaderia_vencimiento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT "FK_mercaderia_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);


--
-- TOC entry 4750 (class 2606 OID 16848)
-- Name: motivo_bloqueo FK_motivo_bloqueo_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT "FK_motivo_bloqueo_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4751 (class 2606 OID 16837)
-- Name: permiso FK_permiso_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT "FK_permiso_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4752 (class 2606 OID 17134)
-- Name: ubicacion FK_ubicacion_extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);


--
-- TOC entry 4753 (class 2606 OID 17129)
-- Name: ubicacion FK_ubicacion_hojalata; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);


--
-- TOC entry 4754 (class 2606 OID 17185)
-- Name: ubicacion FK_ubicacion_insumo_envase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_insumo_envase" FOREIGN KEY (insumo_envase) REFERENCES public.insumo_envase(id);


--
-- TOC entry 4755 (class 2606 OID 17124)
-- Name: ubicacion FK_ubicacion_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);


--
-- TOC entry 4756 (class 2606 OID 17180)
-- Name: ubicacion FK_ubicacion_ubicaciones_nombres; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_ubicaciones_nombres" FOREIGN KEY (ubicacion) REFERENCES public.ubicaciones_nombres(id);


--
-- TOC entry 4757 (class 2606 OID 17139)
-- Name: ubicacion FK_ubicacion_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4758 (class 2606 OID 16882)
-- Name: vencimiento FK_vencimiento_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT "FK_vencimiento_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


-- Completed on 2024-10-07 02:02:33

--
-- PostgreSQL database dump complete
--

