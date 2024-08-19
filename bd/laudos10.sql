--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-08-19 10:30:01

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
-- TOC entry 4875 (class 0 OID 0)
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
    motivo text NOT NULL,
    fecha timestamp with time zone NOT NULL,
    numero_planilla text NOT NULL,
    mercaderia integer NOT NULL,
    responsable integer NOT NULL
);


ALTER TABLE public.bloqueados OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16486)
-- Name: despachos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.despachos (
    id integer NOT NULL,
    mercaderia integer NOT NULL,
    orden_de_entrega integer NOT NULL
);


ALTER TABLE public.despachos OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16533)
-- Name: insumos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insumos (
    id integer NOT NULL,
    fecha_consumo timestamp with time zone NOT NULL,
    producto integer NOT NULL
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
    vencimiento timestamp with time zone,
    lote text NOT NULL,
    lote_cuerpo text,
    lote_tapa text,
    cantidad integer NOT NULL,
    numero_unico text NOT NULL,
    responsable integer NOT NULL
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
    vencimiento timestamp with time zone NOT NULL,
    fecha_elaboracion timestamp with time zone NOT NULL,
    fecha_etiquedato timestamp with time zone NOT NULL,
    lote text NOT NULL,
    responsable integer NOT NULL,
    observacion text,
    numero_unico text NOT NULL
);


ALTER TABLE public.mercaderias OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16466)
-- Name: permisos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permisos (
    id integer NOT NULL,
    mercaderia boolean NOT NULL,
    hojalata boolean NOT NULL,
    ubicacion boolean NOT NULL,
    bloqueo boolean NOT NULL,
    usuario integer NOT NULL,
    partes_de_produccion integer NOT NULL
);


ALTER TABLE public.permisos OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16501)
-- Name: ubicaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicaciones (
    id integer NOT NULL,
    mercaderia integer NOT NULL,
    ubicacion integer NOT NULL,
    responsable integer NOT NULL
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
-- TOC entry 4876 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE usuarios; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.usuarios IS 'informacion de los usuarios';


--
-- TOC entry 4862 (class 0 OID 16425)
-- Dependencies: 219
-- Data for Name: accesos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accesos (id, fecha_acceso, ip, dispotivo, usuario) FROM stdin;
\.


--
-- TOC entry 4859 (class 0 OID 16406)
-- Dependencies: 216
-- Data for Name: arballon_productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arballon_productos (id, codigo, denominacion, clase) FROM stdin;
\.


--
-- TOC entry 4860 (class 0 OID 16413)
-- Dependencies: 217
-- Data for Name: arballon_remitos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arballon_remitos (id, orden_de_entrega) FROM stdin;
\.


--
-- TOC entry 4861 (class 0 OID 16418)
-- Dependencies: 218
-- Data for Name: arballon_ubicaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.arballon_ubicaciones (id, coordenada_1, coordenada_2, coordenada_3, coordenada_4) FROM stdin;
\.


--
-- TOC entry 4864 (class 0 OID 16449)
-- Dependencies: 221
-- Data for Name: bloqueados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bloqueados (id, estado, motivo, fecha, numero_planilla, mercaderia, responsable) FROM stdin;
\.


--
-- TOC entry 4866 (class 0 OID 16486)
-- Dependencies: 223
-- Data for Name: despachos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.despachos (id, mercaderia, orden_de_entrega) FROM stdin;
\.


--
-- TOC entry 4868 (class 0 OID 16533)
-- Dependencies: 225
-- Data for Name: insumos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insumos (id, fecha_consumo, producto) FROM stdin;
\.


--
-- TOC entry 4869 (class 0 OID 16555)
-- Dependencies: 226
-- Data for Name: mercaderia_hojalata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderia_hojalata (id, producto, observacion, fecha_elaboracion, vencimiento, lote, lote_cuerpo, lote_tapa, cantidad, numero_unico, responsable) FROM stdin;
\.


--
-- TOC entry 4863 (class 0 OID 16437)
-- Dependencies: 220
-- Data for Name: mercaderias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mercaderias (id, producto, unidades, vencimiento, fecha_elaboracion, fecha_etiquedato, lote, responsable, observacion, numero_unico) FROM stdin;
\.


--
-- TOC entry 4865 (class 0 OID 16466)
-- Dependencies: 222
-- Data for Name: permisos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permisos (id, mercaderia, hojalata, ubicacion, bloqueo, usuario, partes_de_produccion) FROM stdin;
\.


--
-- TOC entry 4867 (class 0 OID 16501)
-- Dependencies: 224
-- Data for Name: ubicaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicaciones (id, mercaderia, ubicacion, responsable) FROM stdin;
\.


--
-- TOC entry 4858 (class 0 OID 16399)
-- Dependencies: 215
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, contrasena, fecha_creacion, fecha_modificacion, esta_activo) FROM stdin;
\.


--
-- TOC entry 4686 (class 2606 OID 16431)
-- Name: accesos accesos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesos
    ADD CONSTRAINT accesos_pkey PRIMARY KEY (id);


--
-- TOC entry 4680 (class 2606 OID 16412)
-- Name: arballon_productos arballon_producto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arballon_productos
    ADD CONSTRAINT arballon_producto_pkey PRIMARY KEY (id);


--
-- TOC entry 4682 (class 2606 OID 16417)
-- Name: arballon_remitos arballon_remitos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arballon_remitos
    ADD CONSTRAINT arballon_remitos_pkey PRIMARY KEY (id);


--
-- TOC entry 4684 (class 2606 OID 16424)
-- Name: arballon_ubicaciones arballon_ubicaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arballon_ubicaciones
    ADD CONSTRAINT arballon_ubicaciones_pkey PRIMARY KEY (id);


--
-- TOC entry 4690 (class 2606 OID 16455)
-- Name: bloqueados bloqueados_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT bloqueados_pkey PRIMARY KEY (id);


--
-- TOC entry 4694 (class 2606 OID 16490)
-- Name: despachos despachos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT despachos_pkey PRIMARY KEY (id);


--
-- TOC entry 4698 (class 2606 OID 16537)
-- Name: insumos insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_pkey PRIMARY KEY (id);


--
-- TOC entry 4700 (class 2606 OID 16561)
-- Name: mercaderia_hojalata mercaderia_hojalata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT mercaderia_hojalata_pkey PRIMARY KEY (id);


--
-- TOC entry 4688 (class 2606 OID 16443)
-- Name: mercaderias mercaderias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT mercaderias_pkey PRIMARY KEY (id);


--
-- TOC entry 4692 (class 2606 OID 16470)
-- Name: permisos permisos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permisos
    ADD CONSTRAINT permisos_pkey PRIMARY KEY (id);


--
-- TOC entry 4696 (class 2606 OID 16505)
-- Name: ubicaciones ubicaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT ubicaciones_pkey PRIMARY KEY (id);


--
-- TOC entry 4678 (class 2606 OID 16405)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4701 (class 2606 OID 16432)
-- Name: accesos accesos - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesos
    ADD CONSTRAINT "accesos - usuarios" FOREIGN KEY (usuario) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4704 (class 2606 OID 16456)
-- Name: bloqueados bloqueados - mercaderias; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - mercaderias" FOREIGN KEY (mercaderia) REFERENCES public.mercaderias(id) NOT VALID;


--
-- TOC entry 4705 (class 2606 OID 16461)
-- Name: bloqueados bloqueados - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloqueados
    ADD CONSTRAINT "bloqueados - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4707 (class 2606 OID 16491)
-- Name: despachos despachos - mercaderias; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despachos - mercaderias" FOREIGN KEY (mercaderia) REFERENCES public.mercaderias(id) NOT VALID;


--
-- TOC entry 4708 (class 2606 OID 16496)
-- Name: despachos despachos - remitos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.despachos
    ADD CONSTRAINT "despachos - remitos" FOREIGN KEY (orden_de_entrega) REFERENCES public.arballon_remitos(id) NOT VALID;


--
-- TOC entry 4712 (class 2606 OID 16538)
-- Name: insumos insumos - productos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT "insumos - productos" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4713 (class 2606 OID 16562)
-- Name: mercaderia_hojalata merc_hoj - producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT "merc_hoj - producto" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4714 (class 2606 OID 16567)
-- Name: mercaderia_hojalata merc_hoj - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderia_hojalata
    ADD CONSTRAINT "merc_hoj - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4702 (class 2606 OID 16476)
-- Name: mercaderias mercaderias - productos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT "mercaderias - productos" FOREIGN KEY (producto) REFERENCES public.arballon_productos(id) NOT VALID;


--
-- TOC entry 4703 (class 2606 OID 16481)
-- Name: mercaderias mercaderias - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mercaderias
    ADD CONSTRAINT "mercaderias - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4706 (class 2606 OID 16471)
-- Name: permisos permisos - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permisos
    ADD CONSTRAINT "permisos - usuarios" FOREIGN KEY (usuario) REFERENCES public.usuarios(id) NOT VALID;


--
-- TOC entry 4709 (class 2606 OID 16506)
-- Name: ubicaciones ubicaciones - mercaderia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderias(id) NOT VALID;


--
-- TOC entry 4710 (class 2606 OID 16511)
-- Name: ubicaciones ubicaciones - ubicaciones; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - ubicaciones" FOREIGN KEY (ubicacion) REFERENCES public.arballon_ubicaciones(id) NOT VALID;


--
-- TOC entry 4711 (class 2606 OID 16516)
-- Name: ubicaciones ubicaciones - usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT "ubicaciones - usuarios" FOREIGN KEY (responsable) REFERENCES public.usuarios(id) NOT VALID;


-- Completed on 2024-08-19 10:30:01

--
-- PostgreSQL database dump complete
--

