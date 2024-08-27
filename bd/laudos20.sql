--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-08-27 10:06:56

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
-- TOC entry 219 (class 1259 OID 16425)
-- Name: accesos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accesos (
    id integer NOT NULL,
    fecha_acceso timestamp with time zone NOT NULL,
    ip text NOT NULL,
    dispotivo text NOT NULL,
    usuario integer NOT NULL
);


ALTER TABLE public.accesos OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16406)
-- Name: arballon_productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arballon_productos (
    id integer NOT NULL,
    codigo text NOT NULL,
    denominacion text NOT NULL,
    clase text NOT NULL
);


ALTER TABLE public.arballon_productos OWNER TO postgres;

--
-- TOC entry 4912 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE arballon_productos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.arballon_productos IS 'simulacion de la bd arballon tabla productos';


--
-- TOC entry 217 (class 1259 OID 16413)
-- Name: arballon_remitos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arballon_remitos (
    id integer NOT NULL,
    orden_de_entrega integer NOT NULL
);


ALTER TABLE public.arballon_remitos OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16418)
-- Name: arballon_ubicaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arballon_ubicaciones (
    id integer NOT NULL,
    coordenada_1 text NOT NULL,
    coordenada_2 text NOT NULL,
    coordenada_3 text NOT NULL,
    coordenada_4 text NOT NULL
);


ALTER TABLE public.arballon_ubicaciones OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16449)
-- Name: bloqueados; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bloqueados (
    id integer NOT NULL,
    estado boolean NOT NULL,
    fecha timestamp with time zone NOT NULL,
    numero_planilla text NOT NULL,
    mercaderia integer,
    responsable integer NOT NULL,
    mercaderia_hojalata integer,
    observaciones text,
    motivo integer NOT NULL,
    extracto integer
);


ALTER TABLE public.bloqueados OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16486)
-- Name: despachos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.despachos (
    id integer NOT NULL,
    mercaderia integer,
    orden_de_entrega integer NOT NULL,
    mercaderia_hojalata integer,
    fecha timestamp with time zone NOT NULL,
    responsable integer NOT NULL,
    extracto integer
);


ALTER TABLE public.despachos OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16627)
-- Name: extracto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extracto (
    id integer NOT NULL,
    producto integer NOT NULL,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    recipiente text NOT NULL,
    numero_recipiente integer NOT NULL,
    numero_unico text NOT NULL,
    responsable integer NOT NULL,
    observaciones text,
    vencimiento integer NOT NULL
);


ALTER TABLE public.extracto OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16533)
-- Name: insumos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insumos (
    id integer NOT NULL,
    fecha_consumo timestamp with time zone NOT NULL,
    producto integer NOT NULL,
    fecha timestamp with time zone NOT NULL,
    responsable integer NOT NULL,
    numero_unico text NOT NULL
);


ALTER TABLE public.insumos OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16555)
-- Name: mercaderia_hojalata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mercaderia_hojalata (
    id integer NOT NULL,
    producto integer NOT NULL,
    observacion text,
    fecha_elaboracion timestamp with time zone NOT NULL,
    lote text NOT NULL,
    lote_cuerpo text,
    lote_tapa text,
    cantidad integer NOT NULL,
    numero_unico text NOT NULL,
    responsable integer NOT NULL,
    vencimiento integer NOT NULL
);


ALTER TABLE public.mercaderia_hojalata OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16437)
-- Name: mercaderias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mercaderias (
    id integer NOT NULL,
    producto integer NOT NULL,
    unidades integer NOT NULL,
    fecha_elaboracion timestamp with time zone NOT NULL,
    fecha_etiquedato timestamp with time zone NOT NULL,
    lote text NOT NULL,
    responsable integer NOT NULL,
    observacion text,
    numero_unico text NOT NULL,
    insumo integer NOT NULL,
    vencimiento integer NOT NULL
);


ALTER TABLE public.mercaderias OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16597)
-- Name: motivos_bloqueados; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.motivos_bloqueados (
    id integer NOT NULL,
    motivo text NOT NULL,
    producto text NOT NULL
);


ALTER TABLE public.motivos_bloqueados OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16466)
-- Name: permisos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permisos (
    id integer NOT NULL,
    mercaderia boolean NOT NULL,
    mercaderia_hojalata boolean NOT NULL,
    ubicacion boolean NOT NULL,
    bloqueo boolean NOT NULL,
    usuario integer NOT NULL,
    despacho boolean NOT NULL,
    fecha timestamp with time zone NOT NULL,
    insumos boolean NOT NULL,
    extracto boolean NOT NULL
);


ALTER TABLE public.permisos OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16501)
-- Name: ubicaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicaciones (
    id integer NOT NULL,
    mercaderia integer,
    ubicacion integer NOT NULL,
    responsable integer NOT NULL,
    mercaderia_hojalata integer,
    fecha timestamp with time zone NOT NULL,
    extracto integer
);


ALTER TABLE public.ubicaciones OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16399)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre text NOT NULL,
    contrasena text NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_modificacion timestamp with time zone NOT NULL,
    esta_activo boolean NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 4913 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE usuarios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.usuarios IS 'informacion de los usuarios';


--
-- TOC entry 228 (class 1259 OID 16617)
-- Name: vencimientos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vencimientos (
    id integer NOT NULL,
    producto integer NOT NULL,
    meses integer NOT NULL
);


ALTER TABLE public.vencimientos OWNER TO postgres;

--
-- TOC entry 4896 (class 0 OID 16425)
-- Dependencies: 219
-- Data for Name: accesos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accesos (id, fecha_acceso, ip, dispotivo, usuario) FROM stdin;
\.


--
-- TOC entry 4893 (class 0 OID 16406)
-- Dependencies: 216
-- Data for Name: arballon_productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arballon_productos (id, codigo, denominacion, clase) FROM stdin;
\.


--
-- TOC entry 4894 (class 0 OID 16413)
-- Dependencies: 217
-- Data for Name: arballon_remitos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arballon_remitos (id, orden_de_entrega) FROM stdin;
\.


--
-- TOC entry 4895 (class 0 OID 16418)
-- Dependencies: 218
-- Data for Name: arballon_ubicaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arballon_ubicaciones (id, coordenada_1, coordenada_2, coordenada_3, coordenada_4) FROM stdin;
\.


--
-- TOC entry 4898 (class 0 OID 16449)
-- Dependencies: 221
-- Data for Name: bloqueados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bloqueados (id, estado, fecha, numero_planilla, mercaderia, responsable, mercaderia_hojalata, observaciones, motivo, extracto) FROM stdin;
\.


--
-- TOC entry 4900 (class 0 OID 16486)
-- Dependencies: 223
-- Data for Name: despachos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.despachos (id, mercaderia, orden_de_entrega, mercaderia_hojalata, fecha, responsable, extracto) FROM stdin;
\.


--
-- TOC entry 4906 (class 0 OID 16627)
-- Dependencies: 229
-- Data for Name: extracto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extracto (id, producto, fecha_elaboracion, lote, recipiente, numero_recipiente, numero_unico, responsable, observaciones, vencimiento) FROM stdin;
\.


--
-- TOC entry 4902 (class 0 OID 16533)
-- Dependencies: 225
-- Data for Name: insumos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insumos (id, fecha_consumo, producto, fecha, responsable, numero_unico) FROM stdin;
\.


--
-- TOC entry 4903 (class 0 OID 16555)
-- Dependencies: 226
-- Data for Name: mercaderia_hojalata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderia_hojalata (id, producto, observacion, fecha_elaboracion, lote, lote_cuerpo, lote_tapa, cantidad, numero_unico, responsable, vencimiento) FROM stdin;
\.


--
-- TOC entry 4897 (class 0 OID 16437)
-- Dependencies: 220
-- Data for Name: mercaderias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderias (id, producto, unidades, fecha_elaboracion, fecha_etiquedato, lote, responsable, observacion, numero_unico, insumo, vencimiento) FROM stdin;
\.


--
-- TOC entry 4904 (class 0 OID 16597)
-- Dependencies: 227
-- Data for Name: motivos_bloqueados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.motivos_bloqueados (id, motivo, producto) FROM stdin;
\.


--
-- TOC entry 4899 (class 0 OID 16466)
-- Dependencies: 222
-- Data for Name: permisos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permisos (id, mercaderia, mercaderia_hojalata, ubicacion, bloqueo, usuario, despacho, fecha, insumos, extracto) FROM stdin;
\.


--
-- TOC entry 4901 (class 0 OID 16501)
-- Dependencies: 224
-- Data for Name: ubicaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicaciones (id, mercaderia, ubicacion, responsable, mercaderia_hojalata, fecha, extracto) FROM stdin;
\.


--
-- TOC entry 4892 (class 0 OID 16399)
-- Dependencies: 215
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, contrasena, fecha_creacion, fecha_modificacion, esta_activo) FROM stdin;
\.


--
-- TOC entry 4905 (class 0 OID 16617)
-- Dependencies: 228
-- Data for Name: vencimientos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vencimientos (id, producto, meses) FROM stdin;
\.


--
-- TOC entry 4698 (class 2606 OID 16431)
-- Name: accesos accesos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesos
    ADD CONSTRAINT accesos_pkey PRIMARY KEY (id);


--
-- TOC entry 4692 (class 2606 OID 16412)
-- Name: arballon_productos arballon_producto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arballon_productos
    ADD CONSTRAINT arballon_producto_pkey PRIMARY KEY (id);


--
-- TOC entry 4694 (class 2606 OID 16417)
-- Name: arballon_remitos arballon_remitos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arballon_remitos
    ADD CONSTRAINT arballon_remitos_pkey PRIMARY KEY (id);


--
-- TOC entry 4696 (class 2606 OID 16424)
-- Name: arballon_ubicaciones arballon_ubicaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arballon_ubicaciones
    ADD CONSTRAINT arballon_ubicaciones_pkey PRIMARY KEY (id);


--
-- TOC entry 4702 (class 2606 OID 16455)
-- Name: bloqueados bloqueados_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT bloqueados_pkey PRIMARY KEY (id);


--
-- TOC entry 4706 (class 2606 OID 16490)
-- Name: despachos despachos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT despachos_pkey PRIMARY KEY (id);


--
-- TOC entry 4718 (class 2606 OID 16633)
-- Name: extracto extracto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_pkey PRIMARY KEY (id);


--
-- TOC entry 4710 (class 2606 OID 16537)
-- Name: insumos insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_pkey PRIMARY KEY (id);


--
-- TOC entry 4712 (class 2606 OID 16561)
-- Name: mercaderia_hojalata mercaderia_hojalata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT mercaderia_hojalata_pkey PRIMARY KEY (id);


--
-- TOC entry 4700 (class 2606 OID 16443)
-- Name: mercaderias mercaderias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT mercaderias_pkey PRIMARY KEY (id);


--
-- TOC entry 4714 (class 2606 OID 16603)
-- Name: motivos_bloqueados motivos_bloqueados_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.motivos_bloqueados
    ADD CONSTRAINT motivos_bloqueados_pkey PRIMARY KEY (id);


--
-- TOC entry 4704 (class 2606 OID 16470)
-- Name: permisos permisos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permisos
    ADD CONSTRAINT permisos_pkey PRIMARY KEY (id);


--
-- TOC entry 4708 (class 2606 OID 16505)
-- Name: ubicaciones ubicaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT ubicaciones_pkey PRIMARY KEY (id);


--
-- TOC entry 4690 (class 2606 OID 16405)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4716 (class 2606 OID 16621)
-- Name: vencimientos vencimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimientos
    ADD CONSTRAINT vencimientos_pkey PRIMARY KEY (id);


--
-- TOC entry 4719 (class 2606 OID 16432)
-- Name: accesos accesos - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesos
    ADD CONSTRAINT "accesos - usuarios" FOREIGN KEY (usuario) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4724 (class 2606 OID 16644)
-- Name: bloqueados bloqueados - extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id) NOT VALID;


--
-- TOC entry 4725 (class 2606 OID 16572)
-- Name: bloqueados bloqueados - merc_hoj; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - merc_hoj" FOREIGN KEY (mercaderia_hojalata) REFERENCES public.mercaderia_hojalata(id) NOT VALID;


--
-- TOC entry 4726 (class 2606 OID 16456)
-- Name: bloqueados bloqueados - mercaderias; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - mercaderias" FOREIGN KEY (mercaderia) REFERENCES public.mercaderias(id) NOT VALID;


--
-- TOC entry 4727 (class 2606 OID 16604)
-- Name: bloqueados bloqueados - motivos_bloq; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - motivos_bloq" FOREIGN KEY (motivo) REFERENCES public.motivos_bloqueados(id) NOT VALID;


--
-- TOC entry 4728 (class 2606 OID 16461)
-- Name: bloqueados bloqueados - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4730 (class 2606 OID 16587)
-- Name: despachos despacho - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despacho - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4731 (class 2606 OID 16659)
-- Name: despachos despachos - extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despachos - extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id) NOT VALID;


--
-- TOC entry 4732 (class 2606 OID 16577)
-- Name: despachos despachos - merc_hoj; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despachos - merc_hoj" FOREIGN KEY (mercaderia_hojalata) REFERENCES public.mercaderia_hojalata(id) NOT VALID;


--
-- TOC entry 4733 (class 2606 OID 16491)
-- Name: despachos despachos - mercaderias; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despachos - mercaderias" FOREIGN KEY (mercaderia) REFERENCES public.mercaderias(id) NOT VALID;


--
-- TOC entry 4734 (class 2606 OID 16496)
-- Name: despachos despachos - remitos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despachos - remitos" FOREIGN KEY (orden_de_entrega) REFERENCES public.arballon_remitos(id) NOT VALID;


--
-- TOC entry 4746 (class 2606 OID 16634)
-- Name: extracto extracto - producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "extracto - producto" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4747 (class 2606 OID 16639)
-- Name: extracto extracto - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "extracto - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4748 (class 2606 OID 16679)
-- Name: extracto extracto - vencimientos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "extracto - vencimientos" FOREIGN KEY (vencimiento) REFERENCES public.vencimientos(id) NOT VALID;


--
-- TOC entry 4740 (class 2606 OID 16538)
-- Name: insumos insumos - productos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT "insumos - productos" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4741 (class 2606 OID 16592)
-- Name: insumos insumos - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT "insumos - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4742 (class 2606 OID 16674)
-- Name: mercaderia_hojalata mer_hoj - vencimientos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT "mer_hoj - vencimientos" FOREIGN KEY (vencimiento) REFERENCES public.vencimientos(id) NOT VALID;


--
-- TOC entry 4743 (class 2606 OID 16562)
-- Name: mercaderia_hojalata merc_hoj - producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT "merc_hoj - producto" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4744 (class 2606 OID 16567)
-- Name: mercaderia_hojalata merc_hoj - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT "merc_hoj - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4720 (class 2606 OID 16612)
-- Name: mercaderias mercaderias - insumos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT "mercaderias - insumos" FOREIGN KEY (insumo) REFERENCES public.insumos(id) NOT VALID;


--
-- TOC entry 4721 (class 2606 OID 16476)
-- Name: mercaderias mercaderias - productos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT "mercaderias - productos" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4722 (class 2606 OID 16481)
-- Name: mercaderias mercaderias - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT "mercaderias - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4723 (class 2606 OID 16684)
-- Name: mercaderias mercaderias - vencimientos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT "mercaderias - vencimientos" FOREIGN KEY (vencimiento) REFERENCES public.vencimientos(id) NOT VALID;


--
-- TOC entry 4729 (class 2606 OID 16471)
-- Name: permisos permisos - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permisos
    ADD CONSTRAINT "permisos - usuarios" FOREIGN KEY (usuario) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4735 (class 2606 OID 16664)
-- Name: ubicaciones ubicaciones - arb_ubi; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - arb_ubi" FOREIGN KEY (ubicacion) REFERENCES public.arballon_ubicaciones(id) NOT VALID;


--
-- TOC entry 4736 (class 2606 OID 16669)
-- Name: ubicaciones ubicaciones - extracto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id) NOT VALID;


--
-- TOC entry 4737 (class 2606 OID 16582)
-- Name: ubicaciones ubicaciones - merc_hoj; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - merc_hoj" FOREIGN KEY (mercaderia_hojalata) REFERENCES public.mercaderia_hojalata(id) NOT VALID;


--
-- TOC entry 4738 (class 2606 OID 16506)
-- Name: ubicaciones ubicaciones - mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderias(id) NOT VALID;


--
-- TOC entry 4739 (class 2606 OID 16516)
-- Name: ubicaciones ubicaciones - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4745 (class 2606 OID 16622)
-- Name: vencimientos vencimientos - productos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vencimientos
    ADD CONSTRAINT "vencimientos - productos" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


-- Completed on 2024-08-27 10:06:56

--
-- PostgreSQL database dump complete
--

