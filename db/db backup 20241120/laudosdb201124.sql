--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-11-20 00:30:33

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
-- TOC entry 249 (class 1255 OID 25471)
-- Name: verificar_cantidad_aportada(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.verificar_cantidad_aportada() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    cantidad_original INT;
    cantidad_total_aportada INT;
BEGIN
    -- Obtener la cantidad original de la mercadería antecedente
    SELECT cantidad INTO cantidad_original 
    FROM mercaderia 
    WHERE id = NEW.mercaderia_antecedente;

    -- Sumar las cantidades ya aportadas por este antecedente (excluyendo la nueva)
    SELECT COALESCE(SUM(cantidad_tomada), 0) INTO cantidad_total_aportada
    FROM antecedentes 
    WHERE mercaderia_antecedente = NEW.mercaderia_antecedente
      AND id != NEW.id; -- Excluir la fila actual si es una actualización

    -- Agregar la nueva cantidad tomada
    cantidad_total_aportada := cantidad_total_aportada + NEW.cantidad_tomada;

    -- Verificar si la cantidad excede la cantidad original
    IF cantidad_total_aportada > cantidad_original THEN
        RAISE EXCEPTION 'Cantidad total tomada % supera la cantidad original % para el antecedente %',
                        cantidad_total_aportada, cantidad_original, NEW.mercaderia_antecedente;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.verificar_cantidad_aportada() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16722)
-- Name: acceso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acceso (
    id bigint NOT NULL,
    ip text NOT NULL,
    dispositivo text NOT NULL,
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
-- TOC entry 4993 (class 0 OID 0)
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
-- TOC entry 4994 (class 0 OID 0)
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
-- TOC entry 4995 (class 0 OID 0)
-- Dependencies: 219
-- Name: despacho_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.despacho_id_seq OWNED BY public.despacho.id;


--
-- TOC entry 244 (class 1259 OID 25488)
-- Name: tarea_comentario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tarea_comentario (
    id bigint NOT NULL,
    tarea bigint NOT NULL,
    comentario text NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.tarea_comentario OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 25487)
-- Name: estado_tareas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estado_tareas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.estado_tareas_id_seq OWNER TO postgres;

--
-- TOC entry 4996 (class 0 OID 0)
-- Dependencies: 243
-- Name: estado_tareas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estado_tareas_id_seq OWNED BY public.tarea_comentario.id;


--
-- TOC entry 222 (class 1259 OID 16747)
-- Name: extracto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extracto (
    id bigint NOT NULL,
    numero_unico text NOT NULL,
    producto text NOT NULL,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    brix numeric NOT NULL,
    numero_recipiente smallint NOT NULL,
    observaciones text,
    vto_meses bigint NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    den text NOT NULL
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
-- TOC entry 4997 (class 0 OID 0)
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
    producto text NOT NULL,
    observacion text,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    lote_cuerpo text,
    lote_tapa text,
    cantidad integer NOT NULL,
    numero_unico text NOT NULL,
    responsable bigint NOT NULL,
    vto_meses bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    den text NOT NULL
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
-- TOC entry 4998 (class 0 OID 0)
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
    producto text NOT NULL,
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
-- TOC entry 4999 (class 0 OID 0)
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
    producto text NOT NULL,
    observacion text,
    cantidad smallint NOT NULL,
    lote text NOT NULL,
    fecha_elaboracion timestamp with time zone,
    fecha_etiquetado timestamp with time zone,
    responsable bigint NOT NULL,
    numero_unico text NOT NULL,
    vto bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    fecha_encajonado timestamp with time zone,
    den text NOT NULL
);


ALTER TABLE public.mercaderia OWNER TO postgres;

--
-- TOC entry 5000 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE mercaderia; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.mercaderia IS 'v 201124';


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
-- TOC entry 5001 (class 0 OID 0)
-- Dependencies: 227
-- Name: mercaderia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mercaderia_id_seq OWNED BY public.mercaderia.id;


--
-- TOC entry 248 (class 1259 OID 25614)
-- Name: reacondicionado_detalle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reacondicionado_detalle (
    id bigint NOT NULL,
    reacondicionado bigint NOT NULL,
    mercaderia bigint,
    cantidad smallint NOT NULL,
    reacondicionado_detalle bigint,
    fecha_registro timestamp with time zone NOT NULL,
    mercaderia_original bigint NOT NULL
);


ALTER TABLE public.reacondicionado_detalle OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 25613)
-- Name: mezcla_detalle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mezcla_detalle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mezcla_detalle_id_seq OWNER TO postgres;

--
-- TOC entry 5002 (class 0 OID 0)
-- Dependencies: 247
-- Name: mezcla_detalle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mezcla_detalle_id_seq OWNED BY public.reacondicionado_detalle.id;


--
-- TOC entry 246 (class 1259 OID 25600)
-- Name: reacondicionado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reacondicionado (
    id bigint NOT NULL,
    numero_unico text NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    nueva_den text NOT NULL,
    observaciones text,
    tipo_reacondicionado text NOT NULL
);


ALTER TABLE public.reacondicionado OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 25599)
-- Name: mezcla_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mezcla_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mezcla_id_seq OWNER TO postgres;

--
-- TOC entry 5003 (class 0 OID 0)
-- Dependencies: 245
-- Name: mezcla_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mezcla_id_seq OWNED BY public.reacondicionado.id;


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
-- TOC entry 5004 (class 0 OID 0)
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
-- TOC entry 5005 (class 0 OID 0)
-- Dependencies: 231
-- Name: permiso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permiso_id_seq OWNED BY public.permiso.id;


--
-- TOC entry 242 (class 1259 OID 25474)
-- Name: tarea; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tarea (
    id bigint NOT NULL,
    tarea text NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    hecho boolean NOT NULL
);


ALTER TABLE public.tarea OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 25473)
-- Name: tareas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tareas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tareas_id_seq OWNER TO postgres;

--
-- TOC entry 5006 (class 0 OID 0)
-- Dependencies: 241
-- Name: tareas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tareas_id_seq OWNED BY public.tarea.id;


--
-- TOC entry 234 (class 1259 OID 16799)
-- Name: ubicacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicacion (
    id bigint NOT NULL,
    ubicacion_fila bigint NOT NULL,
    mercaderia text,
    hojalata text,
    extracto text,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    insumo_envase text,
    ubicacion_profundidad smallint NOT NULL,
    ubicacion_altura smallint NOT NULL,
    reacondicionado text
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
-- TOC entry 5007 (class 0 OID 0)
-- Dependencies: 233
-- Name: ubicacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicacion_id_seq OWNED BY public.ubicacion.id;


--
-- TOC entry 240 (class 1259 OID 17172)
-- Name: ubicacion_nombre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicacion_nombre (
    id bigint NOT NULL,
    posicion text NOT NULL,
    sector text NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.ubicacion_nombre OWNER TO postgres;

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
-- TOC entry 5008 (class 0 OID 0)
-- Dependencies: 239
-- Name: ubicaciones_nombres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicaciones_nombres_id_seq OWNED BY public.ubicacion_nombre.id;


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
-- TOC entry 5009 (class 0 OID 0)
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
    producto text NOT NULL,
    meses smallint NOT NULL,
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
-- TOC entry 5010 (class 0 OID 0)
-- Dependencies: 237
-- Name: vencimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vencimiento_id_seq OWNED BY public.vencimiento.id;


--
-- TOC entry 4715 (class 2604 OID 16725)
-- Name: acceso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso ALTER COLUMN id SET DEFAULT nextval('public.acceso_id_seq'::regclass);


--
-- TOC entry 4716 (class 2604 OID 16734)
-- Name: bloqueado id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado ALTER COLUMN id SET DEFAULT nextval('public.bloqueado_id_seq'::regclass);


--
-- TOC entry 4717 (class 2604 OID 16743)
-- Name: despacho id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho ALTER COLUMN id SET DEFAULT nextval('public.despacho_id_seq'::regclass);


--
-- TOC entry 4718 (class 2604 OID 16750)
-- Name: extracto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto ALTER COLUMN id SET DEFAULT nextval('public.extracto_id_seq'::regclass);


--
-- TOC entry 4720 (class 2604 OID 16768)
-- Name: hojalata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata ALTER COLUMN id SET DEFAULT nextval('public.hojalata_id_seq'::regclass);


--
-- TOC entry 4719 (class 2604 OID 16759)
-- Name: insumo_envase id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase ALTER COLUMN id SET DEFAULT nextval('public.insumo_id_seq'::regclass);


--
-- TOC entry 4721 (class 2604 OID 16777)
-- Name: mercaderia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia ALTER COLUMN id SET DEFAULT nextval('public.mercaderia_id_seq'::regclass);


--
-- TOC entry 4722 (class 2604 OID 16786)
-- Name: motivo_bloqueo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo ALTER COLUMN id SET DEFAULT nextval('public.motivo_bloqueo_id_seq'::regclass);


--
-- TOC entry 4723 (class 2604 OID 16795)
-- Name: permiso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso ALTER COLUMN id SET DEFAULT nextval('public.permiso_id_seq'::regclass);


--
-- TOC entry 4730 (class 2604 OID 25603)
-- Name: reacondicionado id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado ALTER COLUMN id SET DEFAULT nextval('public.mezcla_id_seq'::regclass);


--
-- TOC entry 4731 (class 2604 OID 25617)
-- Name: reacondicionado_detalle id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado_detalle ALTER COLUMN id SET DEFAULT nextval('public.mezcla_detalle_id_seq'::regclass);


--
-- TOC entry 4728 (class 2604 OID 25477)
-- Name: tarea id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea ALTER COLUMN id SET DEFAULT nextval('public.tareas_id_seq'::regclass);


--
-- TOC entry 4729 (class 2604 OID 25491)
-- Name: tarea_comentario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea_comentario ALTER COLUMN id SET DEFAULT nextval('public.estado_tareas_id_seq'::regclass);


--
-- TOC entry 4724 (class 2604 OID 16802)
-- Name: ubicacion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion ALTER COLUMN id SET DEFAULT nextval('public.ubicacion_id_seq'::regclass);


--
-- TOC entry 4727 (class 2604 OID 17175)
-- Name: ubicacion_nombre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion_nombre ALTER COLUMN id SET DEFAULT nextval('public.ubicaciones_nombres_id_seq'::regclass);


--
-- TOC entry 4725 (class 2604 OID 16809)
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- TOC entry 4726 (class 2604 OID 16819)
-- Name: vencimiento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento ALTER COLUMN id SET DEFAULT nextval('public.vencimiento_id_seq'::regclass);


--
-- TOC entry 4955 (class 0 OID 16722)
-- Dependencies: 216
-- Data for Name: acceso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.acceso (id, ip, dispositivo, usuario, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4957 (class 0 OID 16731)
-- Dependencies: 218
-- Data for Name: bloqueado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bloqueado (id, mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4959 (class 0 OID 16740)
-- Dependencies: 220
-- Data for Name: despacho; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.despacho (id, mercaderia, hojalata, extracto, responsable, fecha_registro, orden_entrega) FROM stdin;
\.


--
-- TOC entry 4961 (class 0 OID 16747)
-- Dependencies: 222
-- Data for Name: extracto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extracto (id, numero_unico, producto, fecha_elaboracion, lote, brix, numero_recipiente, observaciones, vto_meses, responsable, fecha_registro, den) FROM stdin;
\.


--
-- TOC entry 4965 (class 0 OID 16765)
-- Dependencies: 226
-- Data for Name: hojalata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hojalata (id, producto, observacion, fecha_elaboracion, lote, lote_cuerpo, lote_tapa, cantidad, numero_unico, responsable, vto_meses, fecha_registro, den) FROM stdin;
\.


--
-- TOC entry 4963 (class 0 OID 16756)
-- Dependencies: 224
-- Data for Name: insumo_envase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insumo_envase (id, producto, numero_unico, fecha_consumo, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4967 (class 0 OID 16774)
-- Dependencies: 228
-- Data for Name: mercaderia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderia (id, producto, observacion, cantidad, lote, fecha_elaboracion, fecha_etiquetado, responsable, numero_unico, vto, fecha_registro, fecha_encajonado, den) FROM stdin;
\.


--
-- TOC entry 4969 (class 0 OID 16783)
-- Dependencies: 230
-- Data for Name: motivo_bloqueo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.motivo_bloqueo (id, motivo, mercaderia, hojalata, responsable, fecha_registro, extracto) FROM stdin;
2	envase	t	f	1	2024-10-09 10:17:07.770878-03	t
3	aspecto prod	t	f	1	2024-10-09 10:17:07.775672-03	t
4	sellado	t	f	1	2024-10-09 10:17:07.790103-03	t
5	ph alto	t	f	1	2024-10-09 10:17:07.794195-03	t
6	ph bajo	t	f	1	2024-10-09 10:17:07.800066-03	t
7	bajo brix	t	f	1	2024-10-09 10:17:07.819624-03	t
8	esterilizacion	t	f	1	2024-10-09 10:17:07.82474-03	t
9	codificado	t	f	1	2024-10-09 10:17:07.829419-03	t
10	tapado	t	f	1	2024-10-09 10:17:07.835451-03	t
12	remache - filo	f	t	1	2024-10-24 09:38:51.181623-03	f
1	remache - caida	f	t	1	2024-10-09 10:17:07.760839-03	f
13	remache - ganchos cortos	f	t	1	2024-10-24 09:42:17.788436-03	f
14	remache - picos	f	t	1	2024-10-24 09:42:25.482472-03	f
15	costura - desoldada	f	t	1	2024-10-24 09:42:42.15325-03	f
17	costura - quemada en el inicio	f	t	1	2024-10-24 09:43:02.394562-03	f
18	barnizado - desprendimiento	f	t	1	2024-10-24 09:43:35.750658-03	f
19	barnizado - rallado	f	t	1	2024-10-24 09:43:42.028911-03	f
20	barnizado - manchas de grasa	f	t	1	2024-10-24 09:43:48.949507-03	f
21	barnizado - sin barniz	f	t	1	2024-10-24 09:43:55.856327-03	f
22	pestaña - recta	f	t	1	2024-10-24 09:44:09.917234-03	f
23	pestaña - muy inclinada	f	t	1	2024-10-24 09:44:15.904454-03	f
24	otro	t	t	1	2024-10-24 09:44:31.626929-03	t
16	costura - discontinua	f	t	1	2024-10-24 09:42:52.235181-03	f
\.


--
-- TOC entry 4971 (class 0 OID 16792)
-- Dependencies: 232
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permiso (id, mercaderia, hojalata, ubicacion, bloqueo, usuario, despacho, insumo, extracto, acceso, motivo_bloqueo, permiso, vencimiento, responsable, fecha_registro) FROM stdin;
1	t	f	t	t	t	t	t	t	t	t	t	t	1	2024-09-07 17:02:32.860241-03
\.


--
-- TOC entry 4985 (class 0 OID 25600)
-- Dependencies: 246
-- Data for Name: reacondicionado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reacondicionado (id, numero_unico, responsable, fecha_registro, nueva_den, observaciones, tipo_reacondicionado) FROM stdin;
\.


--
-- TOC entry 4987 (class 0 OID 25614)
-- Dependencies: 248
-- Data for Name: reacondicionado_detalle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reacondicionado_detalle (id, reacondicionado, mercaderia, cantidad, reacondicionado_detalle, fecha_registro, mercaderia_original) FROM stdin;
\.


--
-- TOC entry 4981 (class 0 OID 25474)
-- Dependencies: 242
-- Data for Name: tarea; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tarea (id, tarea, responsable, fecha_registro, hecho) FROM stdin;
\.


--
-- TOC entry 4983 (class 0 OID 25488)
-- Dependencies: 244
-- Data for Name: tarea_comentario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tarea_comentario (id, tarea, comentario, responsable, fecha_registro) FROM stdin;
\.


--
-- TOC entry 4973 (class 0 OID 16799)
-- Dependencies: 234
-- Data for Name: ubicacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicacion (id, ubicacion_fila, mercaderia, hojalata, extracto, responsable, fecha_registro, insumo_envase, ubicacion_profundidad, ubicacion_altura, reacondicionado) FROM stdin;
\.


--
-- TOC entry 4979 (class 0 OID 17172)
-- Dependencies: 240
-- Data for Name: ubicacion_nombre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicacion_nombre (id, posicion, sector, fecha_registro) FROM stdin;
1	etiquetado	interior	2024-10-09 13:11:47.177261-03
2	pasillo 1	interior nave 1 y 2	2024-10-09 13:11:47.188242-03
3	pasillo 2	interior nave 2 y 3	2024-10-09 13:11:47.193363-03
4	pasillo 3	interior nave 1, 2 y 3	2024-10-09 13:11:47.196563-03
5	pasillo 1	interior tetra	2024-10-09 13:11:47.201118-03
6	playa norte	exterior norte	2024-10-09 13:11:47.204717-03
7	playa sur	exterior sur	2024-10-09 13:11:47.208853-03
8	playa oeste	exterior oeste	2024-10-09 13:11:47.212664-03
9	rack 1	tetra	2024-10-09 13:11:47.217354-03
10	rack 2	tetra	2024-10-09 13:11:47.220324-03
11	rack 3	tetra	2024-10-09 13:11:47.22365-03
12	rack 4	tetra	2024-10-09 13:11:47.226345-03
13	rack 5	tetra	2024-10-09 13:11:47.229603-03
14	rack 6	tetra	2024-10-09 13:11:47.233477-03
15	rack 7	tetra	2024-10-09 13:11:47.238105-03
16	rack 8	tetra	2024-10-09 13:11:47.24371-03
17	rack 9	tetra	2024-10-09 13:11:47.247284-03
18	rack 10	tetra	2024-10-09 13:11:47.250479-03
19	rack 11	tetra	2024-10-09 13:11:47.253779-03
20	rack 12	tetra	2024-10-09 13:11:47.257285-03
21	rack 13	tetra	2024-10-09 13:11:47.260713-03
22	rack 14	tetra	2024-10-09 13:11:47.264415-03
23	rack 15	tetra	2024-10-09 13:11:47.267631-03
24	rack 16	tetra	2024-10-09 13:11:47.271074-03
25	rack 17	tetra	2024-10-09 13:11:47.274239-03
26	rack 18	tetra	2024-10-09 13:11:47.277654-03
27	rack 19	tetra	2024-10-09 13:11:47.28217-03
28	rack 20	tetra	2024-10-09 13:11:47.285221-03
29	rack 21	tetra	2024-10-09 13:11:47.288106-03
30	rack 22	tetra	2024-10-09 13:11:47.291008-03
31	rack 23	tetra	2024-10-09 13:11:47.294191-03
32	rack 24	tetra	2024-10-09 13:11:47.297864-03
33	rack 25	tetra	2024-10-09 13:11:47.302869-03
34	rack 26	tetra	2024-10-09 13:11:47.306177-03
35	fila 1	nave 1	2024-10-09 13:11:47.308065-03
36	fila 2	nave 1	2024-10-09 13:11:47.309638-03
37	fila 3	nave 1	2024-10-09 13:11:47.311719-03
38	fila 4	nave 1	2024-10-09 13:11:47.31374-03
39	fila 5	nave 1	2024-10-09 13:11:47.316398-03
40	fila 6	nave 1	2024-10-09 13:11:47.318097-03
41	fila 7	nave 1	2024-10-09 13:11:47.31932-03
42	fila 8	nave 1	2024-10-09 13:11:47.321054-03
43	fila 9	nave 1	2024-10-09 13:11:47.323226-03
44	fila 10	nave 1	2024-10-09 13:11:47.324993-03
45	fila 11	nave 1	2024-10-09 13:11:47.326222-03
46	fila 12	nave 1	2024-10-09 13:11:47.32778-03
47	fila 13	nave 1	2024-10-09 13:11:47.329202-03
48	fila 14	nave 1	2024-10-09 13:11:47.331301-03
49	fila 15	nave 1	2024-10-09 13:11:47.333423-03
50	fila 16	nave 1	2024-10-09 13:11:47.335079-03
51	fila 17	nave 1	2024-10-09 13:11:47.336964-03
52	fila 18	nave 1	2024-10-09 13:11:47.338911-03
53	fila 19	nave 1	2024-10-09 13:11:47.340541-03
54	fila 20	nave 1	2024-10-09 13:11:47.341623-03
55	fila 21	nave 1	2024-10-09 13:11:47.343342-03
56	fila 22	nave 1	2024-10-09 13:11:47.345032-03
57	fila 23	nave 1	2024-10-09 13:11:47.347285-03
58	fila 24	nave 1	2024-10-09 13:11:47.349503-03
59	fila 25	nave 1	2024-10-09 13:11:47.351343-03
60	fila 26	nave 1	2024-10-09 13:11:47.35306-03
61	fila 27	nave 1	2024-10-09 13:11:47.377477-03
62	fila 28	nave 1	2024-10-09 13:11:47.379491-03
63	fila 29	nave 1	2024-10-09 13:11:47.382201-03
64	fila 30	nave 1	2024-10-09 13:11:47.384815-03
65	fila 31	nave 1	2024-10-09 13:11:47.387115-03
66	fila 32	nave 1	2024-10-09 13:11:47.389281-03
67	fila 33	nave 1	2024-10-09 13:11:47.391742-03
68	fila 34	nave 1	2024-10-09 13:11:47.393448-03
69	fila 35	nave 1	2024-10-09 13:11:47.394928-03
70	fila 36	nave 1	2024-10-09 13:11:47.396723-03
71	fila 37	nave 1	2024-10-09 13:11:47.398769-03
72	fila 38	nave 1	2024-10-09 13:11:47.400523-03
73	fila 39	nave 1	2024-10-09 13:11:47.402035-03
74	fila 40	nave 1	2024-10-09 13:11:47.404007-03
75	fila 41	nave 1	2024-10-09 13:11:47.405971-03
76	fila 42	nave 1	2024-10-09 13:11:47.408377-03
77	fila 43	nave 1	2024-10-09 13:11:47.410355-03
78	fila 44	nave 1	2024-10-09 13:11:47.412793-03
79	fila 45	nave 1	2024-10-09 13:11:47.414875-03
80	fila 46	nave 1	2024-10-09 13:11:47.417052-03
81	fila 47	nave 1	2024-10-09 13:11:47.418923-03
82	fila 48	nave 1	2024-10-09 13:11:47.420628-03
83	fila 49	nave 1	2024-10-09 13:11:47.422483-03
84	fila 50	nave 1	2024-10-09 13:11:47.440444-03
85	fila 51	nave 1	2024-10-09 13:11:47.442621-03
86	fila 52	nave 1	2024-10-09 13:11:47.444544-03
87	fila 53	nave 1	2024-10-09 13:11:47.446584-03
88	fila 54	nave 1	2024-10-09 13:11:47.449608-03
89	fila 55	nave 1	2024-10-09 13:11:47.451772-03
90	fila 56	nave 1	2024-10-09 13:11:47.453951-03
91	fila 57	nave 1	2024-10-09 13:11:47.456294-03
92	fila 58	nave 2	2024-10-09 13:11:47.45796-03
93	fila 59	nave 2	2024-10-09 13:11:47.459889-03
94	fila 60	nave 2	2024-10-09 13:11:47.461827-03
95	fila 61	nave 2	2024-10-09 13:11:47.463781-03
96	fila 62	nave 2	2024-10-09 13:11:47.466181-03
97	fila 63	nave 2	2024-10-09 13:11:47.468188-03
98	fila 64	nave 2	2024-10-09 13:11:47.470116-03
99	fila 65	nave 2	2024-10-09 13:11:47.471965-03
100	fila 66	nave 2	2024-10-09 13:11:47.473889-03
101	fila 67	nave 2	2024-10-09 13:11:47.475978-03
102	fila 68	nave 2	2024-10-09 13:11:47.477947-03
103	fila 69	nave 2	2024-10-09 13:11:47.480327-03
104	fila 70	nave 2	2024-10-09 13:11:47.482607-03
105	fila 71	nave 2	2024-10-09 13:11:47.503352-03
106	fila 72	nave 2	2024-10-09 13:11:47.505393-03
107	fila 73	nave 2	2024-10-09 13:11:47.507559-03
108	fila 74	nave 2	2024-10-09 13:11:47.509552-03
109	fila 75	nave 2	2024-10-09 13:11:47.511574-03
110	fila 76	nave 2	2024-10-09 13:11:47.513964-03
111	fila 77	nave 2	2024-10-09 13:11:47.51633-03
112	fila 78	nave 2	2024-10-09 13:11:47.519486-03
113	fila 79	nave 2	2024-10-09 13:11:47.521416-03
114	fila 80	nave 2	2024-10-09 13:11:47.523159-03
115	fila 81	nave 2	2024-10-09 13:11:47.524449-03
116	fila 82	nave 2	2024-10-09 13:11:47.526498-03
117	fila 83	nave 2	2024-10-09 13:11:47.528607-03
118	fila 84	nave 2	2024-10-09 13:11:47.530544-03
119	fila 85	nave 2	2024-10-09 13:11:47.532284-03
120	fila 86	nave 2	2024-10-09 13:11:47.534201-03
121	fila 87	nave 2	2024-10-09 13:11:47.536128-03
122	fila 88	nave 2	2024-10-09 13:11:47.537955-03
123	fila 89	nave 2	2024-10-09 13:11:47.540117-03
124	fila 90	nave 2	2024-10-09 13:11:47.542023-03
125	fila 91	nave 2	2024-10-09 13:11:47.543568-03
126	fila 92	nave 2	2024-10-09 13:11:47.544855-03
127	fila 93	nave 2	2024-10-09 13:11:47.547049-03
128	fila 94	nave 2	2024-10-09 13:11:47.549295-03
129	fila 95	nave 2	2024-10-09 13:11:47.551498-03
130	fila 96	nave 2	2024-10-09 13:11:47.553332-03
131	fila 97	nave 2	2024-10-09 13:11:47.555077-03
132	fila 98	nave 2	2024-10-09 13:11:47.556753-03
133	fila 99	nave 2	2024-10-09 13:11:47.558277-03
134	fila 100	nave 2	2024-10-09 13:11:47.559335-03
135	fila 101	nave 2	2024-10-09 13:11:47.561229-03
136	fila 102	nave 2	2024-10-09 13:11:47.566575-03
137	fila 103	nave 2	2024-10-09 13:11:47.568583-03
138	fila 104	nave 2	2024-10-09 13:11:47.570392-03
139	fila 105	nave 2	2024-10-09 13:11:47.572304-03
140	fila 106	nave 2	2024-10-09 13:11:47.574481-03
141	fila 107	nave 2	2024-10-09 13:11:47.576364-03
142	fila 108	nave 2	2024-10-09 13:11:47.578145-03
143	fila 109	nave 2	2024-10-09 13:11:47.580033-03
144	fila 110	nave 2	2024-10-09 13:11:47.582201-03
145	fila 111	nave 2	2024-10-09 13:11:47.58414-03
146	fila 112	nave 2	2024-10-09 13:11:47.58583-03
147	fila 113	nave 2	2024-10-09 13:11:47.588036-03
148	fila 114	nave 2	2024-10-09 13:11:47.589839-03
149	fila 115	nave 2	2024-10-09 13:11:47.59165-03
150	fila 116	nave 2	2024-10-09 13:11:47.594013-03
151	fila 117	nave 2	2024-10-09 13:11:47.595665-03
152	fila 118	nave 2	2024-10-09 13:11:47.59703-03
153	fila 119	nave 2	2024-10-09 13:11:47.599257-03
154	fila 120	nave 2	2024-10-09 13:11:47.601098-03
155	fila 121	nave 2	2024-10-09 13:11:47.602714-03
156	fila 122	nave 2	2024-10-09 13:11:47.604712-03
157	fila 123	nave 2	2024-10-09 13:11:47.606444-03
158	fila 124	nave 2	2024-10-09 13:11:47.608127-03
159	fila 125	nave 2	2024-10-09 13:11:47.609782-03
160	fila 126	nave 2	2024-10-09 13:11:47.611532-03
161	fila 127	nave 2	2024-10-09 13:11:47.613005-03
162	fila 128	nave 2	2024-10-09 13:11:47.61446-03
163	fila 129	nave 2	2024-10-09 13:11:47.617809-03
164	fila 130	nave 2	2024-10-09 13:11:47.620263-03
165	fila 131	nave 2	2024-10-09 13:11:47.622325-03
166	fila 132	nave 2	2024-10-09 13:11:47.624359-03
167	fila 133	nave 2	2024-10-09 13:11:47.626096-03
168	fila 134	nave 2	2024-10-09 13:11:47.627845-03
169	fila 135	nave 2	2024-10-09 13:11:47.629173-03
170	fila 136	nave 2	2024-10-09 13:11:47.630651-03
171	fila 137	nave 2	2024-10-09 13:11:47.631956-03
172	fila 138	nave 2	2024-10-09 13:11:47.632942-03
173	fila 139	nave 2	2024-10-09 13:11:47.633955-03
174	fila 140	nave 2	2024-10-09 13:11:47.634885-03
175	fila 141	nave 2	2024-10-09 13:11:47.636074-03
176	fila 142	nave 2	2024-10-09 13:11:47.637258-03
177	fila 143	nave 2	2024-10-09 13:11:47.638305-03
178	fila 144	nave 2	2024-10-09 13:11:47.639335-03
179	fila 145	nave 2	2024-10-09 13:11:47.640461-03
180	fila 146	nave 2	2024-10-09 13:11:47.641601-03
181	fila 147	nave 2	2024-10-09 13:11:47.642718-03
182	fila 148	nave 2	2024-10-09 13:11:47.644137-03
183	fila 149	nave 2	2024-10-09 13:11:47.646123-03
184	fila 150	nave 2	2024-10-09 13:11:47.647938-03
185	fila 151	nave 2	2024-10-09 13:11:47.650554-03
186	fila 152	nave 2	2024-10-09 13:11:47.652796-03
187	fila 153	nave 2	2024-10-09 13:11:47.654131-03
188	fila 154	nave 2	2024-10-09 13:11:47.656074-03
189	fila 155	nave 2	2024-10-09 13:11:47.657108-03
190	fila 156	nave 2	2024-10-09 13:11:47.65822-03
191	fila 157	nave 2	2024-10-09 13:11:47.659526-03
192	fila 158	nave 2	2024-10-09 13:11:47.661537-03
193	fila 159	nave 2	2024-10-09 13:11:47.662881-03
194	fila 160	nave 2	2024-10-09 13:11:47.665388-03
195	fila 161	nave 2	2024-10-09 13:11:47.66678-03
196	fila 162	nave 2	2024-10-09 13:11:47.668667-03
197	fila 163	nave 2	2024-10-09 13:11:47.66987-03
198	fila 164	nave 3	2024-10-09 13:11:47.672127-03
199	fila 165	nave 3	2024-10-09 13:11:47.674417-03
200	fila 166	nave 3	2024-10-09 13:11:47.676409-03
201	fila 167	nave 3	2024-10-09 13:11:47.677803-03
202	fila 168	nave 3	2024-10-09 13:11:47.679854-03
203	fila 169	nave 3	2024-10-09 13:11:47.681209-03
204	fila 170	nave 3	2024-10-09 13:11:47.682333-03
205	fila 171	nave 3	2024-10-09 13:11:47.683458-03
206	fila 172	nave 3	2024-10-09 13:11:47.684504-03
207	fila 173	nave 3	2024-10-09 13:11:47.685493-03
208	fila 174	nave 3	2024-10-09 13:11:47.686464-03
209	fila 175	nave 3	2024-10-09 13:11:47.687424-03
210	fila 176	nave 3	2024-10-09 13:11:47.688451-03
211	fila 177	nave 3	2024-10-09 13:11:47.69061-03
212	fila 178	nave 3	2024-10-09 13:11:47.692971-03
213	fila 179	nave 3	2024-10-09 13:11:47.695317-03
214	fila 180	nave 3	2024-10-09 13:11:47.697377-03
215	fila 181	nave 3	2024-10-09 13:11:47.698696-03
216	fila 182	nave 3	2024-10-09 13:11:47.699818-03
217	fila 183	nave 3	2024-10-09 13:11:47.701713-03
218	fila 184	nave 3	2024-10-09 13:11:47.703323-03
219	fila 185	nave 3	2024-10-09 13:11:47.705519-03
220	fila 186	nave 3	2024-10-09 13:11:47.707351-03
221	fila 187	nave 3	2024-10-09 13:11:47.709442-03
222	fila 188	nave 3	2024-10-09 13:11:47.710969-03
223	fila 189	nave 3	2024-10-09 13:11:47.712778-03
224	fila 190	nave 3	2024-10-09 13:11:47.71411-03
225	fila 191	nave 3	2024-10-09 13:11:47.716339-03
226	fila 192	nave 3	2024-10-09 13:11:47.717861-03
227	fila 193	nave 3	2024-10-09 13:11:47.719139-03
228	fila 194	nave 3	2024-10-09 13:11:47.72072-03
229	fila 195	nave 3	2024-10-09 13:11:47.722041-03
230	fila 196	nave 3	2024-10-09 13:11:47.72367-03
231	fila 197	nave 3	2024-10-09 13:11:47.725888-03
232	fila 198	nave 3	2024-10-09 13:11:47.727383-03
233	fila 199	nave 3	2024-10-09 13:11:47.729072-03
234	fila 200	nave 3	2024-10-09 13:11:47.730927-03
235	fila 201	nave 3	2024-10-09 13:11:47.733069-03
236	fila 202	nave 3	2024-10-09 13:11:47.757874-03
237	fila 203	nave 3	2024-10-09 13:11:47.760082-03
238	fila 204	nave 3	2024-10-09 13:11:47.761996-03
239	fila 205	nave 3	2024-10-09 13:11:47.764352-03
240	fila 206	nave 3	2024-10-09 13:11:47.767135-03
241	fila 207	nave 3	2024-10-09 13:11:47.769454-03
242	fila 208	nave 3	2024-10-09 13:11:47.771991-03
243	fila 209	nave 3	2024-10-09 13:11:47.773316-03
244	fila 210	nave 3	2024-10-09 13:11:47.775191-03
245	fila 211	nave 3	2024-10-09 13:11:47.777081-03
246	fila 212	nave 3	2024-10-09 13:11:47.778863-03
247	fila 213	nave 3	2024-10-09 13:11:47.780205-03
248	fila 214	nave 3	2024-10-09 13:11:47.781546-03
249	fila 215	nave 3	2024-10-09 13:11:47.783425-03
250	fila 216	nave 3	2024-10-09 13:11:47.785221-03
251	fila 217	nave 3	2024-10-09 13:11:47.787043-03
252	fila 218	nave 3	2024-10-09 13:11:47.78875-03
253	fila 219	nave 3	2024-10-09 13:11:47.791338-03
254	fila 220	nave 3	2024-10-09 13:11:47.793105-03
255	fila 221	nave 1 - sector 1	2024-10-09 13:11:47.795176-03
256	fila 222	nave 1 - sector 1	2024-10-09 13:11:47.797301-03
257	fila 223	nave 1 - sector 1	2024-10-09 13:11:47.799564-03
258	fila 224	nave 1 - sector 1	2024-10-09 13:11:47.801199-03
259	fila 225	nave 1 - sector 1	2024-10-09 13:11:47.803268-03
260	fila 226	nave 1 - sector 1	2024-10-09 13:11:47.805368-03
261	fila 227	nave 1 - sector 1	2024-10-09 13:11:47.807261-03
262	fila 228	nave 1 - sector 1	2024-10-09 13:11:47.809363-03
263	fila 229	nave 1 - sector 1	2024-10-09 13:11:47.810896-03
264	fila 230	nave 1 - sector 1	2024-10-09 13:11:47.81265-03
265	fila 231	nave 1 - sector 1	2024-10-09 13:11:47.814135-03
266	fila 232	nave 1 - sector 1	2024-10-09 13:11:47.816526-03
267	fila 233	nave 1 - sector 1	2024-10-09 13:11:47.818345-03
268	fila 234	nave 1 - sector 1	2024-10-09 13:11:47.820115-03
269	fila 235	nave 1 - sector 1	2024-10-09 13:11:47.821823-03
270	fila 236	nave 1 - sector 1	2024-10-09 13:11:47.823538-03
271	fila 237	nave 1 - sector 1	2024-10-09 13:11:47.825198-03
272	fila 238	nave 1 - sector 1	2024-10-09 13:11:47.827716-03
273	fila 239	nave 1 - sector 1	2024-10-09 13:11:47.829287-03
274	fila 240	nave 1 - sector 1	2024-10-09 13:11:47.830984-03
275	fila 241	nave 1 - sector 1	2024-10-09 13:11:47.833097-03
276	fila 242	nave 1 - sector 1	2024-10-09 13:11:47.834984-03
277	fila 243	nave 1 - sector 1	2024-10-09 13:11:47.836711-03
278	fila 244	nave 2 - sector 1	2024-10-09 13:11:47.838338-03
279	fila 245	nave 2 - sector 1	2024-10-09 13:11:47.840022-03
280	fila 246	nave 2 - sector 1	2024-10-09 13:11:47.841711-03
281	fila 247	nave 2 - sector 1	2024-10-09 13:11:47.843841-03
282	fila 248	nave 2 - sector 1	2024-10-09 13:11:47.845763-03
283	fila 249	nave 2 - sector 1	2024-10-09 13:11:47.85015-03
284	fila 250	nave 2 - sector 1	2024-10-09 13:11:47.852479-03
285	fila 251	nave 2 - sector 1	2024-10-09 13:11:47.854897-03
286	fila 252	nave 2 - sector 1	2024-10-09 13:11:47.85669-03
287	fila 253	nave 2 - sector 1	2024-10-09 13:11:47.859352-03
288	fila 254	nave 2 - sector 1	2024-10-09 13:11:47.860712-03
289	fila 255	nave 2 - sector 1	2024-10-09 13:11:47.862019-03
290	fila 256	nave 2 - sector 1	2024-10-09 13:11:47.864357-03
291	fila 257	nave 2 - sector 1	2024-10-09 13:11:47.865436-03
292	fila 258	nave 2 - sector 1	2024-10-09 13:11:47.866357-03
293	fila 259	nave 2 - sector 1	2024-10-09 13:11:47.867261-03
294	fila 260	nave 2 - sector 1	2024-10-09 13:11:47.868125-03
295	fila 261	nave 2 - sector 1	2024-10-09 13:11:47.868976-03
296	fila 262	nave 2 - sector 1	2024-10-09 13:11:47.869881-03
297	fila 263	nave 2 - sector 1	2024-10-09 13:11:47.871122-03
298	fila 264	nave 3 - sector 1	2024-10-09 13:11:47.872963-03
299	fila 265	nave 3 - sector 1	2024-10-09 13:11:47.874153-03
300	fila 266	nave 3 - sector 1	2024-10-09 13:11:47.87582-03
301	fila 267	nave 3 - sector 1	2024-10-09 13:11:47.877037-03
302	fila 268	nave 3 - sector 1	2024-10-09 13:11:47.878354-03
303	fila 269	nave 3 - sector 1	2024-10-09 13:11:47.881208-03
304	fila 270	nave 3 - sector 1	2024-10-09 13:11:47.882299-03
305	fila 271	nave 3 - sector 1	2024-10-09 13:11:47.883567-03
306	fila 272	nave 3 - sector 1	2024-10-09 13:11:47.885468-03
307	fila 273	nave 3 - sector 1	2024-10-09 13:11:47.887302-03
308	fila 274	nave 3 - sector 1	2024-10-09 13:11:47.888802-03
309	fila 275	nave 3 - sector 1	2024-10-09 13:11:47.890068-03
310	fila 276	nave 3 - sector 1	2024-10-09 13:11:47.891671-03
311	fila 277	nave 3 - sector 1	2024-10-09 13:11:47.893673-03
312	fila 278	nave 3 - sector 1	2024-10-09 13:11:47.895278-03
313	fila 279	nave 3 - sector 1	2024-10-09 13:11:47.896409-03
314	fila 280	nave 3 - sector 1	2024-10-09 13:11:47.897938-03
315	fila 281	nave 3 - sector 1	2024-10-09 13:11:47.900038-03
316	fila 282	nave 3 - sector 1	2024-10-09 13:11:47.901863-03
317	fila 283	nave 3 - sector 1	2024-10-09 13:11:47.903453-03
318	fila 284	nave 3 - sector 1	2024-10-09 13:11:47.905471-03
\.


--
-- TOC entry 4975 (class 0 OID 16806)
-- Dependencies: 236
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id, nombre, password, fecha_creacion, fecha_modificacion, esta_activo) FROM stdin;
1	laureano	abc123	2024-09-07 15:20:02.852177-03	2024-09-07 15:20:02.852177-03	t
\.


--
-- TOC entry 4977 (class 0 OID 16816)
-- Dependencies: 238
-- Data for Name: vencimiento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vencimiento (id, producto, meses, responsable, fecha_registro) FROM stdin;
4	Extrac	24	1	2024-10-09 09:58:36.796713-03
5	Pas500	36	1	2024-10-09 09:58:36.803806-03
6	Pelado	24	1	2024-10-09 09:58:36.808787-03
7	Pulpa	24	1	2024-10-09 09:58:36.813571-03
8	Pure	18	1	2024-10-09 09:58:36.818221-03
9	Tri500	36	1	2024-10-09 09:58:36.825543-03
10	Tri8	24	1	2024-10-09 09:58:36.830539-03
11	Tri910	36	1	2024-10-09 09:58:36.834629-03
12	Tri950	36	1	2024-10-09 09:58:36.841096-03
\.


--
-- TOC entry 5011 (class 0 OID 0)
-- Dependencies: 215
-- Name: acceso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.acceso_id_seq', 176, true);


--
-- TOC entry 5012 (class 0 OID 0)
-- Dependencies: 217
-- Name: bloqueado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bloqueado_id_seq', 1, false);


--
-- TOC entry 5013 (class 0 OID 0)
-- Dependencies: 219
-- Name: despacho_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.despacho_id_seq', 1, false);


--
-- TOC entry 5014 (class 0 OID 0)
-- Dependencies: 243
-- Name: estado_tareas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estado_tareas_id_seq', 1, false);


--
-- TOC entry 5015 (class 0 OID 0)
-- Dependencies: 221
-- Name: extracto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extracto_id_seq', 19, true);


--
-- TOC entry 5016 (class 0 OID 0)
-- Dependencies: 225
-- Name: hojalata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hojalata_id_seq', 1, false);


--
-- TOC entry 5017 (class 0 OID 0)
-- Dependencies: 223
-- Name: insumo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.insumo_id_seq', 1, false);


--
-- TOC entry 5018 (class 0 OID 0)
-- Dependencies: 227
-- Name: mercaderia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mercaderia_id_seq', 154, true);


--
-- TOC entry 5019 (class 0 OID 0)
-- Dependencies: 247
-- Name: mezcla_detalle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mezcla_detalle_id_seq', 139, true);


--
-- TOC entry 5020 (class 0 OID 0)
-- Dependencies: 245
-- Name: mezcla_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mezcla_id_seq', 77, true);


--
-- TOC entry 5021 (class 0 OID 0)
-- Dependencies: 229
-- Name: motivo_bloqueo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.motivo_bloqueo_id_seq', 24, true);


--
-- TOC entry 5022 (class 0 OID 0)
-- Dependencies: 231
-- Name: permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permiso_id_seq', 1, true);


--
-- TOC entry 5023 (class 0 OID 0)
-- Dependencies: 241
-- Name: tareas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tareas_id_seq', 1, false);


--
-- TOC entry 5024 (class 0 OID 0)
-- Dependencies: 233
-- Name: ubicacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicacion_id_seq', 20, true);


--
-- TOC entry 5025 (class 0 OID 0)
-- Dependencies: 239
-- Name: ubicaciones_nombres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicaciones_nombres_id_seq', 318, true);


--
-- TOC entry 5026 (class 0 OID 0)
-- Dependencies: 235
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_seq', 1, true);


--
-- TOC entry 5027 (class 0 OID 0)
-- Dependencies: 237
-- Name: vencimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vencimiento_id_seq', 12, true);


--
-- TOC entry 4733 (class 2606 OID 16729)
-- Name: acceso acceso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT acceso_pkey PRIMARY KEY (id);


--
-- TOC entry 4735 (class 2606 OID 16738)
-- Name: bloqueado bloqueado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT bloqueado_pkey PRIMARY KEY (id);


--
-- TOC entry 4737 (class 2606 OID 16745)
-- Name: despacho despacho_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT despacho_pkey PRIMARY KEY (id);


--
-- TOC entry 4769 (class 2606 OID 25495)
-- Name: tarea_comentario estado_tareas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea_comentario
    ADD CONSTRAINT estado_tareas_pkey PRIMARY KEY (id);


--
-- TOC entry 4739 (class 2606 OID 25414)
-- Name: extracto extracto_numero_unico; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_numero_unico UNIQUE (numero_unico);


--
-- TOC entry 4741 (class 2606 OID 16754)
-- Name: extracto extracto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_pkey PRIMARY KEY (id);


--
-- TOC entry 4747 (class 2606 OID 25412)
-- Name: hojalata hojalata_numero_unico; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT hojalata_numero_unico UNIQUE (numero_unico);


--
-- TOC entry 4749 (class 2606 OID 16772)
-- Name: hojalata hojalata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT hojalata_pkey PRIMARY KEY (id);


--
-- TOC entry 4743 (class 2606 OID 25410)
-- Name: insumo_envase insumo_envase_numero_unico; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT insumo_envase_numero_unico UNIQUE (numero_unico);


--
-- TOC entry 4745 (class 2606 OID 16763)
-- Name: insumo_envase insumo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT insumo_pkey PRIMARY KEY (id);


--
-- TOC entry 4751 (class 2606 OID 16781)
-- Name: mercaderia mercaderia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT mercaderia_pkey PRIMARY KEY (id);


--
-- TOC entry 4775 (class 2606 OID 25619)
-- Name: reacondicionado_detalle mezcla_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT mezcla_detalle_pkey PRIMARY KEY (id);


--
-- TOC entry 4771 (class 2606 OID 25607)
-- Name: reacondicionado mezcla_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado
    ADD CONSTRAINT mezcla_pkey PRIMARY KEY (id);


--
-- TOC entry 4755 (class 2606 OID 16790)
-- Name: motivo_bloqueo motivo_bloqueo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT motivo_bloqueo_pkey PRIMARY KEY (id);


--
-- TOC entry 4773 (class 2606 OID 25711)
-- Name: reacondicionado numero_unico_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado
    ADD CONSTRAINT numero_unico_unique UNIQUE (numero_unico);


--
-- TOC entry 4757 (class 2606 OID 16797)
-- Name: permiso permiso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT permiso_pkey PRIMARY KEY (id);


--
-- TOC entry 4767 (class 2606 OID 25481)
-- Name: tarea tareas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea
    ADD CONSTRAINT tareas_pkey PRIMARY KEY (id);


--
-- TOC entry 4759 (class 2606 OID 16804)
-- Name: ubicacion ubicacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT ubicacion_pkey PRIMARY KEY (id);


--
-- TOC entry 4765 (class 2606 OID 17177)
-- Name: ubicacion_nombre ubicaciones_nombres_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion_nombre
    ADD CONSTRAINT ubicaciones_nombres_pkey PRIMARY KEY (id);


--
-- TOC entry 4753 (class 2606 OID 25408)
-- Name: mercaderia unique_numero_unico; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT unique_numero_unico UNIQUE (numero_unico);


--
-- TOC entry 4761 (class 2606 OID 16813)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- TOC entry 4763 (class 2606 OID 16821)
-- Name: vencimiento vencimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT vencimiento_pkey PRIMARY KEY (id);


--
-- TOC entry 4807 (class 2606 OID 25635)
-- Name: reacondicionado_detalle FK__mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK__mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);


--
-- TOC entry 4808 (class 2606 OID 25660)
-- Name: reacondicionado_detalle FK__mezcla; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK__mezcla" FOREIGN KEY (reacondicionado) REFERENCES public.reacondicionado(id);


--
-- TOC entry 4804 (class 2606 OID 25496)
-- Name: tarea_comentario FK__tareas; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea_comentario
    ADD CONSTRAINT "FK__tareas" FOREIGN KEY (tarea) REFERENCES public.tarea(id);


--
-- TOC entry 4803 (class 2606 OID 25482)
-- Name: tarea FK__usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea
    ADD CONSTRAINT "FK__usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4805 (class 2606 OID 25501)
-- Name: tarea_comentario FK__usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarea_comentario
    ADD CONSTRAINT "FK__usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4806 (class 2606 OID 25608)
-- Name: reacondicionado FK__usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado
    ADD CONSTRAINT "FK__usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4776 (class 2606 OID 16828)
-- Name: acceso FK_acceso_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT "FK_acceso_usuario" FOREIGN KEY (usuario) REFERENCES public.usuario(id);


--
-- TOC entry 4777 (class 2606 OID 17047)
-- Name: bloqueado FK_bloqueado_extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);


--
-- TOC entry 4778 (class 2606 OID 17042)
-- Name: bloqueado FK_bloqueado_hojalata; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);


--
-- TOC entry 4779 (class 2606 OID 17037)
-- Name: bloqueado FK_bloqueado_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);


--
-- TOC entry 4780 (class 2606 OID 17032)
-- Name: bloqueado FK_bloqueado_motivo_bloqueo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_motivo_bloqueo" FOREIGN KEY (motivo) REFERENCES public.motivo_bloqueo(id);


--
-- TOC entry 4781 (class 2606 OID 17027)
-- Name: bloqueado FK_bloqueado_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4782 (class 2606 OID 17082)
-- Name: despacho FK_despacho_extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);


--
-- TOC entry 4783 (class 2606 OID 17077)
-- Name: despacho FK_despacho_hojalata; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);


--
-- TOC entry 4784 (class 2606 OID 17072)
-- Name: despacho FK_despacho_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);


--
-- TOC entry 4785 (class 2606 OID 17087)
-- Name: despacho FK_despacho_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4786 (class 2606 OID 16951)
-- Name: extracto FK_extracto_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "FK_extracto_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4787 (class 2606 OID 16946)
-- Name: extracto FK_extracto_vencimiento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "FK_extracto_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);


--
-- TOC entry 4789 (class 2606 OID 16917)
-- Name: hojalata FK_hojalata_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT "FK_hojalata_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4790 (class 2606 OID 16912)
-- Name: hojalata FK_hojalata_vencimiento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT "FK_hojalata_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);


--
-- TOC entry 4788 (class 2606 OID 16865)
-- Name: insumo_envase FK_insumo_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT "FK_insumo_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4791 (class 2606 OID 16974)
-- Name: mercaderia FK_mercaderia_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT "FK_mercaderia_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4792 (class 2606 OID 17204)
-- Name: mercaderia FK_mercaderia_vencimiento; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT "FK_mercaderia_vencimiento" FOREIGN KEY (vto) REFERENCES public.vencimiento(id);


--
-- TOC entry 4809 (class 2606 OID 25665)
-- Name: reacondicionado_detalle FK_mezcla_detalle_mezcla_detalle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK_mezcla_detalle_mezcla_detalle" FOREIGN KEY (reacondicionado_detalle) REFERENCES public.reacondicionado_detalle(id);


--
-- TOC entry 4793 (class 2606 OID 16848)
-- Name: motivo_bloqueo FK_motivo_bloqueo_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT "FK_motivo_bloqueo_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4794 (class 2606 OID 16837)
-- Name: permiso FK_permiso_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT "FK_permiso_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4810 (class 2606 OID 25675)
-- Name: reacondicionado_detalle FK_reacondicionado_detalle_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK_reacondicionado_detalle_mercaderia" FOREIGN KEY (mercaderia_original) REFERENCES public.mercaderia(id);


--
-- TOC entry 4795 (class 2606 OID 25747)
-- Name: ubicacion FK_ubicacion_extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(numero_unico);


--
-- TOC entry 4796 (class 2606 OID 25742)
-- Name: ubicacion FK_ubicacion_hojalata; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(numero_unico);


--
-- TOC entry 4797 (class 2606 OID 25752)
-- Name: ubicacion FK_ubicacion_insumo_envase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_insumo_envase" FOREIGN KEY (insumo_envase) REFERENCES public.insumo_envase(numero_unico);


--
-- TOC entry 4798 (class 2606 OID 25737)
-- Name: ubicacion FK_ubicacion_mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(numero_unico);


--
-- TOC entry 4799 (class 2606 OID 25757)
-- Name: ubicacion FK_ubicacion_reacondicionado; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_reacondicionado" FOREIGN KEY (reacondicionado) REFERENCES public.reacondicionado(numero_unico);


--
-- TOC entry 4800 (class 2606 OID 25670)
-- Name: ubicacion FK_ubicacion_ubicaciones_nombres; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_ubicaciones_nombres" FOREIGN KEY (ubicacion_fila) REFERENCES public.ubicacion_nombre(id);


--
-- TOC entry 4801 (class 2606 OID 17139)
-- Name: ubicacion FK_ubicacion_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


--
-- TOC entry 4802 (class 2606 OID 16882)
-- Name: vencimiento FK_vencimiento_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT "FK_vencimiento_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);


-- Completed on 2024-11-20 00:30:33

--
-- PostgreSQL database dump complete
--

