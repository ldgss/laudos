--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-09-07 17:08:37

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
    usuario integer NOT NULL,
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
-- TOC entry 4897 (class 0 OID 0)
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
    mercaderia integer,
    hojalata integer,
    extracto integer,
    estado boolean NOT NULL,
    numero_planilla text NOT NULL,
    motivo integer NOT NULL,
    observaciones text,
    responsable integer NOT NULL,
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
-- TOC entry 4898 (class 0 OID 0)
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
    mercaderia integer,
    hojalata integer,
    extracto integer,
    responsable integer NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    orden_entrega integer
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
-- TOC entry 4899 (class 0 OID 0)
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
    productro integer NOT NULL,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    recipiente text NOT NULL,
    numero_recipiente integer NOT NULL,
    observaciones text,
    vto_meses integer NOT NULL,
    responsable integer NOT NULL
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
-- TOC entry 4900 (class 0 OID 0)
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
    producto integer NOT NULL,
    observacion text,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    lote_cuerpo text,
    lote_tapa text,
    cantidad integer NOT NULL,
    numero_unico text NOT NULL,
    responsable integer NOT NULL,
    vto_meses integer NOT NULL,
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
-- TOC entry 4901 (class 0 OID 0)
-- Dependencies: 225
-- Name: hojalata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hojalata_id_seq OWNED BY public.hojalata.id;


--
-- TOC entry 224 (class 1259 OID 16756)
-- Name: insumo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insumo (
    id bigint NOT NULL,
    producto integer NOT NULL,
    numero_unico text NOT NULL,
    fecha_consumo timestamp with time zone NOT NULL,
    responsable integer NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.insumo OWNER TO postgres;

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
-- TOC entry 4902 (class 0 OID 0)
-- Dependencies: 223
-- Name: insumo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.insumo_id_seq OWNED BY public.insumo.id;


--
-- TOC entry 228 (class 1259 OID 16774)
-- Name: mercaderia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mercaderia (
    id bigint NOT NULL,
    producto integer NOT NULL,
    observacion text,
    cantidad integer NOT NULL,
    lote text NOT NULL,
    fecha_elaboracion timestamp with time zone,
    fecha_etiquetado timestamp with time zone,
    responsable integer NOT NULL,
    numero_unico text NOT NULL,
    vto_meses integer NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
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
-- TOC entry 4903 (class 0 OID 0)
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
    responsable integer NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
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
-- TOC entry 4904 (class 0 OID 0)
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
    responsable integer NOT NULL,
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
-- TOC entry 4905 (class 0 OID 0)
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
    ubicacion integer NOT NULL,
    mercaderia integer,
    hojalata integer,
    extracto integer,
    responsable integer NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
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
-- TOC entry 4906 (class 0 OID 0)
-- Dependencies: 233
-- Name: ubicacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicacion_id_seq OWNED BY public.ubicacion.id;


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
-- TOC entry 4907 (class 0 OID 0)
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
    producto integer NOT NULL,
    meses integer NOT NULL,
    responsable integer NOT NULL,
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
-- TOC entry 4908 (class 0 OID 0)
-- Dependencies: 237
-- Name: vencimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vencimiento_id_seq OWNED BY public.vencimiento.id;


--
-- TOC entry 4689 (class 2604 OID 16725)
-- Name: acceso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso ALTER COLUMN id SET DEFAULT nextval('public.acceso_id_seq'::regclass);


--
-- TOC entry 4690 (class 2604 OID 16734)
-- Name: bloqueado id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado ALTER COLUMN id SET DEFAULT nextval('public.bloqueado_id_seq'::regclass);


--
-- TOC entry 4691 (class 2604 OID 16743)
-- Name: despacho id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho ALTER COLUMN id SET DEFAULT nextval('public.despacho_id_seq'::regclass);


--
-- TOC entry 4692 (class 2604 OID 16750)
-- Name: extracto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto ALTER COLUMN id SET DEFAULT nextval('public.extracto_id_seq'::regclass);


--
-- TOC entry 4694 (class 2604 OID 16768)
-- Name: hojalata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata ALTER COLUMN id SET DEFAULT nextval('public.hojalata_id_seq'::regclass);


--
-- TOC entry 4693 (class 2604 OID 16759)
-- Name: insumo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo ALTER COLUMN id SET DEFAULT nextval('public.insumo_id_seq'::regclass);


--
-- TOC entry 4695 (class 2604 OID 16777)
-- Name: mercaderia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia ALTER COLUMN id SET DEFAULT nextval('public.mercaderia_id_seq'::regclass);


--
-- TOC entry 4696 (class 2604 OID 16786)
-- Name: motivo_bloqueo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo ALTER COLUMN id SET DEFAULT nextval('public.motivo_bloqueo_id_seq'::regclass);


--
-- TOC entry 4697 (class 2604 OID 16795)
-- Name: permiso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso ALTER COLUMN id SET DEFAULT nextval('public.permiso_id_seq'::regclass);


--
-- TOC entry 4698 (class 2604 OID 16802)
-- Name: ubicacion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion ALTER COLUMN id SET DEFAULT nextval('public.ubicacion_id_seq'::regclass);


--
-- TOC entry 4699 (class 2604 OID 16809)
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- TOC entry 4700 (class 2604 OID 16819)
-- Name: vencimiento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento ALTER COLUMN id SET DEFAULT nextval('public.vencimiento_id_seq'::regclass);


--
-- TOC entry 4869 (class 0 OID 16722)
-- Dependencies: 216
-- Data for Name: acceso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.acceso (id, ip, dispositvo, usuario, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4871 (class 0 OID 16731)
-- Dependencies: 218
-- Data for Name: bloqueado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bloqueado (id, mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4873 (class 0 OID 16740)
-- Dependencies: 220
-- Data for Name: despacho; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.despacho (id, mercaderia, hojalata, extracto, responsable, fecha_registro, orden_entrega) FROM stdin;
\.


--
-- TOC entry 4875 (class 0 OID 16747)
-- Dependencies: 222
-- Data for Name: extracto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extracto (id, numero_unico, productro, fecha_elaboracion, lote, recipiente, numero_recipiente, observaciones, vto_meses, responsable) FROM stdin;
\.


--
-- TOC entry 4879 (class 0 OID 16765)
-- Dependencies: 226
-- Data for Name: hojalata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hojalata (id, producto, observacion, fecha_elaboracion, lote, lote_cuerpo, lote_tapa, cantidad, numero_unico, responsable, vto_meses, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4877 (class 0 OID 16756)
-- Dependencies: 224
-- Data for Name: insumo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insumo (id, producto, numero_unico, fecha_consumo, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4881 (class 0 OID 16774)
-- Dependencies: 228
-- Data for Name: mercaderia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderia (id, producto, observacion, cantidad, lote, fecha_elaboracion, fecha_etiquetado, responsable, numero_unico, vto_meses, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4883 (class 0 OID 16783)
-- Dependencies: 230
-- Data for Name: motivo_bloqueo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.motivo_bloqueo (id, motivo, mercaderia, hojalata, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4885 (class 0 OID 16792)
-- Dependencies: 232
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permiso (id, mercaderia, hojalata, ubicacion, bloqueo, usuario, despacho, insumo, extracto, acceso, motivo_bloqueo, permiso, vencimiento, responsable, fecha_registro) FROM stdin;
1	t	f	t	t	t	t	t	f	t	t	t	t	1	2024-09-07 17:02:32.860241-03
\.


--
-- TOC entry 4887 (class 0 OID 16799)
-- Dependencies: 234
-- Data for Name: ubicacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicacion (id, ubicacion, mercaderia, hojalata, extracto, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4889 (class 0 OID 16806)
-- Dependencies: 236
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id, nombre, password, fecha_creacion, fecha_modificacion, esta_activo) FROM stdin;
1	laureano	abc123	2024-09-07 15:20:02.852177-03	2024-09-07 15:20:02.852177-03	t
\.


--
-- TOC entry 4891 (class 0 OID 16816)
-- Dependencies: 238
-- Data for Name: vencimiento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vencimiento (id, producto, meses, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4909 (class 0 OID 0)
-- Dependencies: 215
-- Name: acceso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.acceso_id_seq', 1, false);


--
-- TOC entry 4910 (class 0 OID 0)
-- Dependencies: 217
-- Name: bloqueado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bloqueado_id_seq', 1, false);


--
-- TOC entry 4911 (class 0 OID 0)
-- Dependencies: 219
-- Name: despacho_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.despacho_id_seq', 1, false);


--
-- TOC entry 4912 (class 0 OID 0)
-- Dependencies: 221
-- Name: extracto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extracto_id_seq', 1, false);


--
-- TOC entry 4913 (class 0 OID 0)
-- Dependencies: 225
-- Name: hojalata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hojalata_id_seq', 1, false);


--
-- TOC entry 4914 (class 0 OID 0)
-- Dependencies: 223
-- Name: insumo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.insumo_id_seq', 1, false);


--
-- TOC entry 4915 (class 0 OID 0)
-- Dependencies: 227
-- Name: mercaderia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mercaderia_id_seq', 1, false);


--
-- TOC entry 4916 (class 0 OID 0)
-- Dependencies: 229
-- Name: motivo_bloqueo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.motivo_bloqueo_id_seq', 1, false);


--
-- TOC entry 4917 (class 0 OID 0)
-- Dependencies: 231
-- Name: permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permiso_id_seq', 1, true);


--
-- TOC entry 4918 (class 0 OID 0)
-- Dependencies: 233
-- Name: ubicacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicacion_id_seq', 1, false);


--
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 235
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_seq', 1, true);


--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 237
-- Name: vencimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vencimiento_id_seq', 1, false);


--
-- TOC entry 4702 (class 2606 OID 16729)
-- Name: acceso acceso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT acceso_pkey PRIMARY KEY (id);


--
-- TOC entry 4704 (class 2606 OID 16738)
-- Name: bloqueado bloqueado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT bloqueado_pkey PRIMARY KEY (id);


--
-- TOC entry 4706 (class 2606 OID 16745)
-- Name: despacho despacho_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT despacho_pkey PRIMARY KEY (id);


--
-- TOC entry 4708 (class 2606 OID 16754)
-- Name: extracto extracto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_pkey PRIMARY KEY (id);


--
-- TOC entry 4712 (class 2606 OID 16772)
-- Name: hojalata hojalata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT hojalata_pkey PRIMARY KEY (id);


--
-- TOC entry 4710 (class 2606 OID 16763)
-- Name: insumo insumo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo
    ADD CONSTRAINT insumo_pkey PRIMARY KEY (id);


--
-- TOC entry 4714 (class 2606 OID 16781)
-- Name: mercaderia mercaderia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT mercaderia_pkey PRIMARY KEY (id);


--
-- TOC entry 4716 (class 2606 OID 16790)
-- Name: motivo_bloqueo motivo_bloqueo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT motivo_bloqueo_pkey PRIMARY KEY (id);


--
-- TOC entry 4718 (class 2606 OID 16797)
-- Name: permiso permiso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT permiso_pkey PRIMARY KEY (id);


--
-- TOC entry 4720 (class 2606 OID 16804)
-- Name: ubicacion ubicacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT ubicacion_pkey PRIMARY KEY (id);


--
-- TOC entry 4722 (class 2606 OID 16813)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- TOC entry 4724 (class 2606 OID 16821)
-- Name: vencimiento vencimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT vencimiento_pkey PRIMARY KEY (id);


-- Completed on 2024-09-07 17:08:37

--
-- PostgreSQL database dump complete
--

