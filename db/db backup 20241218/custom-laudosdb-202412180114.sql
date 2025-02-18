PGDMP                      |            laudosdb     16.4 (Ubuntu 16.4-1.pgdg22.04+2)    16.3 �    �           0    0    ENCODING    ENCODING     #   SET client_encoding = 'SQL_ASCII';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24577    laudosdb    DATABASE     o   CREATE DATABASE laudosdb WITH TEMPLATE = template0 ENCODING = 'SQL_ASCII' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE laudosdb;
                laudosdbdba    false            �           0    0    laudosdb    DATABASE PROPERTIES     G   ALTER DATABASE laudosdb SET "TimeZone" TO 'America/Argentina/Mendoza';
                     laudosdbdba    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1255    24579    verificar_cantidad_aportada()    FUNCTION     �  CREATE FUNCTION public.verificar_cantidad_aportada() RETURNS trigger
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
 4   DROP FUNCTION public.verificar_cantidad_aportada();
       public          laudosdbdba    false    4            �            1259    24580    acceso    TABLE     �   CREATE TABLE public.acceso (
    id bigint NOT NULL,
    ip text NOT NULL,
    dispositivo text NOT NULL,
    usuario bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);
    DROP TABLE public.acceso;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE acceso    ACL     I   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.acceso TO laudosdbusr;
          public          laudosdbdba    false    215            �            1259    24585    acceso_id_seq    SEQUENCE     v   CREATE SEQUENCE public.acceso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.acceso_id_seq;
       public          laudosdbdba    false    215    4            �           0    0    acceso_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.acceso_id_seq OWNED BY public.acceso.id;
          public          laudosdbdba    false    216            �           0    0    SEQUENCE acceso_id_seq    ACL     =   GRANT USAGE ON SEQUENCE public.acceso_id_seq TO laudosdbusr;
          public          laudosdbdba    false    216            �            1259    24586 	   bloqueado    TABLE     F  CREATE TABLE public.bloqueado (
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
    DROP TABLE public.bloqueado;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE bloqueado    ACL     L   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.bloqueado TO laudosdbusr;
          public          laudosdbdba    false    217            �            1259    24591    bloqueado_id_seq    SEQUENCE     y   CREATE SEQUENCE public.bloqueado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.bloqueado_id_seq;
       public          laudosdbdba    false    217    4            �           0    0    bloqueado_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.bloqueado_id_seq OWNED BY public.bloqueado.id;
          public          laudosdbdba    false    218            �           0    0    SEQUENCE bloqueado_id_seq    ACL     @   GRANT USAGE ON SEQUENCE public.bloqueado_id_seq TO laudosdbusr;
          public          laudosdbdba    false    218            �            1259    24592    despacho    TABLE     �   CREATE TABLE public.despacho (
    id bigint NOT NULL,
    mercaderia bigint,
    hojalata bigint,
    extracto bigint,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    orden_entrega bigint
);
    DROP TABLE public.despacho;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE despacho    ACL     K   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.despacho TO laudosdbusr;
          public          laudosdbdba    false    219            �            1259    24595    despacho_id_seq    SEQUENCE     x   CREATE SEQUENCE public.despacho_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.despacho_id_seq;
       public          laudosdbdba    false    4    219            �           0    0    despacho_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.despacho_id_seq OWNED BY public.despacho.id;
          public          laudosdbdba    false    220            �           0    0    SEQUENCE despacho_id_seq    ACL     ?   GRANT USAGE ON SEQUENCE public.despacho_id_seq TO laudosdbusr;
          public          laudosdbdba    false    220            �            1259    24596    tarea_comentario    TABLE     �   CREATE TABLE public.tarea_comentario (
    id bigint NOT NULL,
    tarea bigint NOT NULL,
    comentario text NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);
 $   DROP TABLE public.tarea_comentario;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE tarea_comentario    ACL     S   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.tarea_comentario TO laudosdbusr;
          public          laudosdbdba    false    221            �            1259    24601    estado_tareas_id_seq    SEQUENCE     }   CREATE SEQUENCE public.estado_tareas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.estado_tareas_id_seq;
       public          laudosdbdba    false    4    221            �           0    0    estado_tareas_id_seq    SEQUENCE OWNED BY     P   ALTER SEQUENCE public.estado_tareas_id_seq OWNED BY public.tarea_comentario.id;
          public          laudosdbdba    false    222            �           0    0    SEQUENCE estado_tareas_id_seq    ACL     D   GRANT USAGE ON SEQUENCE public.estado_tareas_id_seq TO laudosdbusr;
          public          laudosdbdba    false    222            �            1259    24602    extracto    TABLE     �  CREATE TABLE public.extracto (
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
    DROP TABLE public.extracto;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE extracto    ACL     K   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.extracto TO laudosdbusr;
          public          laudosdbdba    false    223            �            1259    24607    extracto_id_seq    SEQUENCE     x   CREATE SEQUENCE public.extracto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.extracto_id_seq;
       public          laudosdbdba    false    4    223            �           0    0    extracto_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.extracto_id_seq OWNED BY public.extracto.id;
          public          laudosdbdba    false    224            �           0    0    SEQUENCE extracto_id_seq    ACL     ?   GRANT USAGE ON SEQUENCE public.extracto_id_seq TO laudosdbusr;
          public          laudosdbdba    false    224            �            1259    24608    hojalata    TABLE     �  CREATE TABLE public.hojalata (
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
    DROP TABLE public.hojalata;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE hojalata    ACL     K   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.hojalata TO laudosdbusr;
          public          laudosdbdba    false    225            �            1259    24613    hojalata_id_seq    SEQUENCE     x   CREATE SEQUENCE public.hojalata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.hojalata_id_seq;
       public          laudosdbdba    false    225    4            �           0    0    hojalata_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.hojalata_id_seq OWNED BY public.hojalata.id;
          public          laudosdbdba    false    226            �           0    0    SEQUENCE hojalata_id_seq    ACL     ?   GRANT USAGE ON SEQUENCE public.hojalata_id_seq TO laudosdbusr;
          public          laudosdbdba    false    226            �            1259    24614    insumo_envase    TABLE     D  CREATE TABLE public.insumo_envase (
    id bigint NOT NULL,
    insumo text NOT NULL,
    codigo_insumo text NOT NULL,
    fecha_consumo timestamp with time zone NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    lote_insumo text NOT NULL,
    cantidad smallint NOT NULL
);
 !   DROP TABLE public.insumo_envase;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE insumo_envase    ACL     P   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.insumo_envase TO laudosdbusr;
          public          laudosdbdba    false    227            �            1259    24619    insumo_id_seq    SEQUENCE     v   CREATE SEQUENCE public.insumo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.insumo_id_seq;
       public          laudosdbdba    false    227    4            �           0    0    insumo_id_seq    SEQUENCE OWNED BY     F   ALTER SEQUENCE public.insumo_id_seq OWNED BY public.insumo_envase.id;
          public          laudosdbdba    false    228            �           0    0    SEQUENCE insumo_id_seq    ACL     =   GRANT USAGE ON SEQUENCE public.insumo_id_seq TO laudosdbusr;
          public          laudosdbdba    false    228            �            1259    24620 
   mercaderia    TABLE     �  CREATE TABLE public.mercaderia (
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
    DROP TABLE public.mercaderia;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE mercaderia    COMMENT     2   COMMENT ON TABLE public.mercaderia IS 'v 201124';
          public          laudosdbdba    false    229            �           0    0    TABLE mercaderia    ACL     M   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.mercaderia TO laudosdbusr;
          public          laudosdbdba    false    229            �            1259    24625    mercaderia_id_seq    SEQUENCE     z   CREATE SEQUENCE public.mercaderia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.mercaderia_id_seq;
       public          laudosdbdba    false    229    4            �           0    0    mercaderia_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.mercaderia_id_seq OWNED BY public.mercaderia.id;
          public          laudosdbdba    false    230            �           0    0    SEQUENCE mercaderia_id_seq    ACL     A   GRANT USAGE ON SEQUENCE public.mercaderia_id_seq TO laudosdbusr;
          public          laudosdbdba    false    230            �            1259    24626    reacondicionado_detalle    TABLE     '  CREATE TABLE public.reacondicionado_detalle (
    id bigint NOT NULL,
    reacondicionado bigint NOT NULL,
    mercaderia bigint,
    cantidad smallint NOT NULL,
    reacondicionado_detalle bigint,
    fecha_registro timestamp with time zone NOT NULL,
    mercaderia_original bigint NOT NULL
);
 +   DROP TABLE public.reacondicionado_detalle;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE reacondicionado_detalle    ACL     Z   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.reacondicionado_detalle TO laudosdbusr;
          public          laudosdbdba    false    231            �            1259    24629    mezcla_detalle_id_seq    SEQUENCE     ~   CREATE SEQUENCE public.mezcla_detalle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.mezcla_detalle_id_seq;
       public          laudosdbdba    false    231    4            �           0    0    mezcla_detalle_id_seq    SEQUENCE OWNED BY     X   ALTER SEQUENCE public.mezcla_detalle_id_seq OWNED BY public.reacondicionado_detalle.id;
          public          laudosdbdba    false    232            �           0    0    SEQUENCE mezcla_detalle_id_seq    ACL     E   GRANT USAGE ON SEQUENCE public.mezcla_detalle_id_seq TO laudosdbusr;
          public          laudosdbdba    false    232            �            1259    24630    reacondicionado    TABLE       CREATE TABLE public.reacondicionado (
    id bigint NOT NULL,
    numero_unico text NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    nueva_den text NOT NULL,
    observaciones text,
    tipo_reacondicionado text NOT NULL
);
 #   DROP TABLE public.reacondicionado;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE reacondicionado    ACL     R   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.reacondicionado TO laudosdbusr;
          public          laudosdbdba    false    233            �            1259    24635    mezcla_id_seq    SEQUENCE     v   CREATE SEQUENCE public.mezcla_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.mezcla_id_seq;
       public          laudosdbdba    false    233    4            �           0    0    mezcla_id_seq    SEQUENCE OWNED BY     H   ALTER SEQUENCE public.mezcla_id_seq OWNED BY public.reacondicionado.id;
          public          laudosdbdba    false    234            �           0    0    SEQUENCE mezcla_id_seq    ACL     =   GRANT USAGE ON SEQUENCE public.mezcla_id_seq TO laudosdbusr;
          public          laudosdbdba    false    234            �            1259    24636    motivo_bloqueo    TABLE       CREATE TABLE public.motivo_bloqueo (
    id bigint NOT NULL,
    motivo text NOT NULL,
    mercaderia boolean NOT NULL,
    hojalata boolean NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    extracto boolean NOT NULL
);
 "   DROP TABLE public.motivo_bloqueo;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE motivo_bloqueo    ACL     Q   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.motivo_bloqueo TO laudosdbusr;
          public          laudosdbdba    false    235            �            1259    24641    motivo_bloqueo_id_seq    SEQUENCE     ~   CREATE SEQUENCE public.motivo_bloqueo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.motivo_bloqueo_id_seq;
       public          laudosdbdba    false    4    235            �           0    0    motivo_bloqueo_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.motivo_bloqueo_id_seq OWNED BY public.motivo_bloqueo.id;
          public          laudosdbdba    false    236            �           0    0    SEQUENCE motivo_bloqueo_id_seq    ACL     E   GRANT USAGE ON SEQUENCE public.motivo_bloqueo_id_seq TO laudosdbusr;
          public          laudosdbdba    false    236            �            1259    24642    permiso    TABLE       CREATE TABLE public.permiso (
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
    DROP TABLE public.permiso;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE permiso    ACL     J   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.permiso TO laudosdbusr;
          public          laudosdbdba    false    237            �            1259    24645    permiso_id_seq    SEQUENCE     w   CREATE SEQUENCE public.permiso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.permiso_id_seq;
       public          laudosdbdba    false    237    4            �           0    0    permiso_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.permiso_id_seq OWNED BY public.permiso.id;
          public          laudosdbdba    false    238            �           0    0    SEQUENCE permiso_id_seq    ACL     >   GRANT USAGE ON SEQUENCE public.permiso_id_seq TO laudosdbusr;
          public          laudosdbdba    false    238            �            1259    24646    tarea    TABLE     �   CREATE TABLE public.tarea (
    id bigint NOT NULL,
    tarea text NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL,
    hecho boolean NOT NULL
);
    DROP TABLE public.tarea;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE tarea    ACL     H   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.tarea TO laudosdbusr;
          public          laudosdbdba    false    239            �            1259    24651    tareas_id_seq    SEQUENCE     v   CREATE SEQUENCE public.tareas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.tareas_id_seq;
       public          laudosdbdba    false    239    4            �           0    0    tareas_id_seq    SEQUENCE OWNED BY     >   ALTER SEQUENCE public.tareas_id_seq OWNED BY public.tarea.id;
          public          laudosdbdba    false    240            �           0    0    SEQUENCE tareas_id_seq    ACL     =   GRANT USAGE ON SEQUENCE public.tareas_id_seq TO laudosdbusr;
          public          laudosdbdba    false    240            �            1259    24652 	   ubicacion    TABLE     w  CREATE TABLE public.ubicacion (
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
    DROP TABLE public.ubicacion;
       public         heap    laudosdbdba    false    4            �           0    0    TABLE ubicacion    ACL     L   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.ubicacion TO laudosdbusr;
          public          laudosdbdba    false    241            �            1259    24657    ubicacion_id_seq    SEQUENCE     y   CREATE SEQUENCE public.ubicacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.ubicacion_id_seq;
       public          laudosdbdba    false    241    4                        0    0    ubicacion_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.ubicacion_id_seq OWNED BY public.ubicacion.id;
          public          laudosdbdba    false    242                       0    0    SEQUENCE ubicacion_id_seq    ACL     @   GRANT USAGE ON SEQUENCE public.ubicacion_id_seq TO laudosdbusr;
          public          laudosdbdba    false    242            �            1259    24658    ubicacion_nombre    TABLE     �   CREATE TABLE public.ubicacion_nombre (
    id bigint NOT NULL,
    posicion text NOT NULL,
    sector text NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);
 $   DROP TABLE public.ubicacion_nombre;
       public         heap    laudosdbdba    false    4                       0    0    TABLE ubicacion_nombre    ACL     S   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.ubicacion_nombre TO laudosdbusr;
          public          laudosdbdba    false    243            �            1259    24663    ubicaciones_nombres_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ubicaciones_nombres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.ubicaciones_nombres_id_seq;
       public          laudosdbdba    false    4    243                       0    0    ubicaciones_nombres_id_seq    SEQUENCE OWNED BY     V   ALTER SEQUENCE public.ubicaciones_nombres_id_seq OWNED BY public.ubicacion_nombre.id;
          public          laudosdbdba    false    244                       0    0 #   SEQUENCE ubicaciones_nombres_id_seq    ACL     J   GRANT USAGE ON SEQUENCE public.ubicaciones_nombres_id_seq TO laudosdbusr;
          public          laudosdbdba    false    244            �            1259    24664    usuario    TABLE        CREATE TABLE public.usuario (
    id bigint NOT NULL,
    nombre text NOT NULL,
    password text NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_modificacion timestamp with time zone NOT NULL,
    esta_activo boolean NOT NULL
);
    DROP TABLE public.usuario;
       public         heap    laudosdbdba    false    4                       0    0    TABLE usuario    ACL     J   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.usuario TO laudosdbusr;
          public          laudosdbdba    false    245            �            1259    24669    usuario_id_seq    SEQUENCE     w   CREATE SEQUENCE public.usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.usuario_id_seq;
       public          laudosdbdba    false    245    4                       0    0    usuario_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;
          public          laudosdbdba    false    246                       0    0    SEQUENCE usuario_id_seq    ACL     >   GRANT USAGE ON SEQUENCE public.usuario_id_seq TO laudosdbusr;
          public          laudosdbdba    false    246            �            1259    24670    vencimiento    TABLE     �   CREATE TABLE public.vencimiento (
    id bigint NOT NULL,
    producto text NOT NULL,
    meses smallint NOT NULL,
    responsable bigint NOT NULL,
    fecha_registro timestamp with time zone NOT NULL
);
    DROP TABLE public.vencimiento;
       public         heap    laudosdbdba    false    4                       0    0    TABLE vencimiento    ACL     N   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.vencimiento TO laudosdbusr;
          public          laudosdbdba    false    247            �            1259    24675    vencimiento_id_seq    SEQUENCE     {   CREATE SEQUENCE public.vencimiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.vencimiento_id_seq;
       public          laudosdbdba    false    4    247            	           0    0    vencimiento_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.vencimiento_id_seq OWNED BY public.vencimiento.id;
          public          laudosdbdba    false    248            
           0    0    SEQUENCE vencimiento_id_seq    ACL     B   GRANT USAGE ON SEQUENCE public.vencimiento_id_seq TO laudosdbusr;
          public          laudosdbdba    false    248            �           2604    24930 	   acceso id    DEFAULT     f   ALTER TABLE ONLY public.acceso ALTER COLUMN id SET DEFAULT nextval('public.acceso_id_seq'::regclass);
 8   ALTER TABLE public.acceso ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    216    215            �           2604    24931    bloqueado id    DEFAULT     l   ALTER TABLE ONLY public.bloqueado ALTER COLUMN id SET DEFAULT nextval('public.bloqueado_id_seq'::regclass);
 ;   ALTER TABLE public.bloqueado ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    218    217            �           2604    24932    despacho id    DEFAULT     j   ALTER TABLE ONLY public.despacho ALTER COLUMN id SET DEFAULT nextval('public.despacho_id_seq'::regclass);
 :   ALTER TABLE public.despacho ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    220    219            �           2604    24933    extracto id    DEFAULT     j   ALTER TABLE ONLY public.extracto ALTER COLUMN id SET DEFAULT nextval('public.extracto_id_seq'::regclass);
 :   ALTER TABLE public.extracto ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    224    223            �           2604    24934    hojalata id    DEFAULT     j   ALTER TABLE ONLY public.hojalata ALTER COLUMN id SET DEFAULT nextval('public.hojalata_id_seq'::regclass);
 :   ALTER TABLE public.hojalata ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    226    225            �           2604    24935    insumo_envase id    DEFAULT     m   ALTER TABLE ONLY public.insumo_envase ALTER COLUMN id SET DEFAULT nextval('public.insumo_id_seq'::regclass);
 ?   ALTER TABLE public.insumo_envase ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    228    227            �           2604    24936    mercaderia id    DEFAULT     n   ALTER TABLE ONLY public.mercaderia ALTER COLUMN id SET DEFAULT nextval('public.mercaderia_id_seq'::regclass);
 <   ALTER TABLE public.mercaderia ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    230    229            �           2604    24937    motivo_bloqueo id    DEFAULT     v   ALTER TABLE ONLY public.motivo_bloqueo ALTER COLUMN id SET DEFAULT nextval('public.motivo_bloqueo_id_seq'::regclass);
 @   ALTER TABLE public.motivo_bloqueo ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    236    235            �           2604    24938 
   permiso id    DEFAULT     h   ALTER TABLE ONLY public.permiso ALTER COLUMN id SET DEFAULT nextval('public.permiso_id_seq'::regclass);
 9   ALTER TABLE public.permiso ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    238    237            �           2604    24939    reacondicionado id    DEFAULT     o   ALTER TABLE ONLY public.reacondicionado ALTER COLUMN id SET DEFAULT nextval('public.mezcla_id_seq'::regclass);
 A   ALTER TABLE public.reacondicionado ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    234    233            �           2604    24940    reacondicionado_detalle id    DEFAULT        ALTER TABLE ONLY public.reacondicionado_detalle ALTER COLUMN id SET DEFAULT nextval('public.mezcla_detalle_id_seq'::regclass);
 I   ALTER TABLE public.reacondicionado_detalle ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    232    231            �           2604    24941    tarea id    DEFAULT     e   ALTER TABLE ONLY public.tarea ALTER COLUMN id SET DEFAULT nextval('public.tareas_id_seq'::regclass);
 7   ALTER TABLE public.tarea ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    240    239            �           2604    24942    tarea_comentario id    DEFAULT     w   ALTER TABLE ONLY public.tarea_comentario ALTER COLUMN id SET DEFAULT nextval('public.estado_tareas_id_seq'::regclass);
 B   ALTER TABLE public.tarea_comentario ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    222    221            �           2604    24943    ubicacion id    DEFAULT     l   ALTER TABLE ONLY public.ubicacion ALTER COLUMN id SET DEFAULT nextval('public.ubicacion_id_seq'::regclass);
 ;   ALTER TABLE public.ubicacion ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    242    241            �           2604    24944    ubicacion_nombre id    DEFAULT     }   ALTER TABLE ONLY public.ubicacion_nombre ALTER COLUMN id SET DEFAULT nextval('public.ubicaciones_nombres_id_seq'::regclass);
 B   ALTER TABLE public.ubicacion_nombre ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    244    243            �           2604    24945 
   usuario id    DEFAULT     h   ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);
 9   ALTER TABLE public.usuario ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    246    245            �           2604    24946    vencimiento id    DEFAULT     p   ALTER TABLE ONLY public.vencimiento ALTER COLUMN id SET DEFAULT nextval('public.vencimiento_id_seq'::regclass);
 =   ALTER TABLE public.vencimiento ALTER COLUMN id DROP DEFAULT;
       public          laudosdbdba    false    248    247            �          0    24580    acceso 
   TABLE DATA           N   COPY public.acceso (id, ip, dispositivo, usuario, fecha_registro) FROM stdin;
    public          laudosdbdba    false    215   ��       �          0    24586 	   bloqueado 
   TABLE DATA           �   COPY public.bloqueado (id, mercaderia, hojalata, extracto, estado, numero_planilla, motivo, observaciones, responsable, fecha_registro) FROM stdin;
    public          laudosdbdba    false    217   ��       �          0    24592    despacho 
   TABLE DATA           r   COPY public.despacho (id, mercaderia, hojalata, extracto, responsable, fecha_registro, orden_entrega) FROM stdin;
    public          laudosdbdba    false    219   �       �          0    24602    extracto 
   TABLE DATA           �   COPY public.extracto (id, numero_unico, producto, fecha_elaboracion, lote, brix, numero_recipiente, observaciones, vto_meses, responsable, fecha_registro, den) FROM stdin;
    public          laudosdbdba    false    223   "�       �          0    24608    hojalata 
   TABLE DATA           �   COPY public.hojalata (id, producto, observacion, fecha_elaboracion, lote, lote_cuerpo, lote_tapa, cantidad, numero_unico, responsable, vto_meses, fecha_registro, den) FROM stdin;
    public          laudosdbdba    false    225   ?�       �          0    24614    insumo_envase 
   TABLE DATA           �   COPY public.insumo_envase (id, insumo, codigo_insumo, fecha_consumo, responsable, fecha_registro, lote_insumo, cantidad) FROM stdin;
    public          laudosdbdba    false    227   \�       �          0    24620 
   mercaderia 
   TABLE DATA           �   COPY public.mercaderia (id, producto, observacion, cantidad, lote, fecha_elaboracion, fecha_etiquetado, responsable, numero_unico, vto, fecha_registro, fecha_encajonado, den) FROM stdin;
    public          laudosdbdba    false    229   y�       �          0    24636    motivo_bloqueo 
   TABLE DATA           q   COPY public.motivo_bloqueo (id, motivo, mercaderia, hojalata, responsable, fecha_registro, extracto) FROM stdin;
    public          laudosdbdba    false    235   ��       �          0    24642    permiso 
   TABLE DATA           �   COPY public.permiso (id, mercaderia, hojalata, ubicacion, bloqueo, usuario, despacho, insumo, extracto, acceso, motivo_bloqueo, permiso, vencimiento, responsable, fecha_registro) FROM stdin;
    public          laudosdbdba    false    237   ��       �          0    24630    reacondicionado 
   TABLE DATA           �   COPY public.reacondicionado (id, numero_unico, responsable, fecha_registro, nueva_den, observaciones, tipo_reacondicionado) FROM stdin;
    public          laudosdbdba    false    233   ��       �          0    24626    reacondicionado_detalle 
   TABLE DATA           �   COPY public.reacondicionado_detalle (id, reacondicionado, mercaderia, cantidad, reacondicionado_detalle, fecha_registro, mercaderia_original) FROM stdin;
    public          laudosdbdba    false    231   ��       �          0    24646    tarea 
   TABLE DATA           N   COPY public.tarea (id, tarea, responsable, fecha_registro, hecho) FROM stdin;
    public          laudosdbdba    false    239   ��       �          0    24596    tarea_comentario 
   TABLE DATA           ^   COPY public.tarea_comentario (id, tarea, comentario, responsable, fecha_registro) FROM stdin;
    public          laudosdbdba    false    221   �       �          0    24652 	   ubicacion 
   TABLE DATA           �   COPY public.ubicacion (id, ubicacion_fila, mercaderia, hojalata, extracto, responsable, fecha_registro, insumo_envase, ubicacion_profundidad, ubicacion_altura, reacondicionado) FROM stdin;
    public          laudosdbdba    false    241   6�       �          0    24658    ubicacion_nombre 
   TABLE DATA           P   COPY public.ubicacion_nombre (id, posicion, sector, fecha_registro) FROM stdin;
    public          laudosdbdba    false    243   S�       �          0    24664    usuario 
   TABLE DATA           h   COPY public.usuario (id, nombre, password, fecha_creacion, fecha_modificacion, esta_activo) FROM stdin;
    public          laudosdbdba    false    245   �      �          0    24670    vencimiento 
   TABLE DATA           W   COPY public.vencimiento (id, producto, meses, responsable, fecha_registro) FROM stdin;
    public          laudosdbdba    false    247   �                 0    0    acceso_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.acceso_id_seq', 326, true);
          public          laudosdbdba    false    216                       0    0    bloqueado_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.bloqueado_id_seq', 1, false);
          public          laudosdbdba    false    218                       0    0    despacho_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.despacho_id_seq', 1, false);
          public          laudosdbdba    false    220                       0    0    estado_tareas_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.estado_tareas_id_seq', 1, false);
          public          laudosdbdba    false    222                       0    0    extracto_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.extracto_id_seq', 22, true);
          public          laudosdbdba    false    224                       0    0    hojalata_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.hojalata_id_seq', 1, false);
          public          laudosdbdba    false    226                       0    0    insumo_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.insumo_id_seq', 4, true);
          public          laudosdbdba    false    228                       0    0    mercaderia_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.mercaderia_id_seq', 184, true);
          public          laudosdbdba    false    230                       0    0    mezcla_detalle_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.mezcla_detalle_id_seq', 167, true);
          public          laudosdbdba    false    232                       0    0    mezcla_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.mezcla_id_seq', 91, true);
          public          laudosdbdba    false    234                       0    0    motivo_bloqueo_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.motivo_bloqueo_id_seq', 24, true);
          public          laudosdbdba    false    236                       0    0    permiso_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.permiso_id_seq', 20, true);
          public          laudosdbdba    false    238                       0    0    tareas_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.tareas_id_seq', 1, false);
          public          laudosdbdba    false    240                       0    0    ubicacion_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.ubicacion_id_seq', 46, true);
          public          laudosdbdba    false    242                       0    0    ubicaciones_nombres_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.ubicaciones_nombres_id_seq', 318, true);
          public          laudosdbdba    false    244                       0    0    usuario_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.usuario_id_seq', 19, true);
          public          laudosdbdba    false    246                       0    0    vencimiento_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.vencimiento_id_seq', 12, true);
          public          laudosdbdba    false    248            �           2606    24694    acceso acceso_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT acceso_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.acceso DROP CONSTRAINT acceso_pkey;
       public            laudosdbdba    false    215            �           2606    24696    bloqueado bloqueado_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT bloqueado_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.bloqueado DROP CONSTRAINT bloqueado_pkey;
       public            laudosdbdba    false    217            �           2606    24698    despacho despacho_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT despacho_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.despacho DROP CONSTRAINT despacho_pkey;
       public            laudosdbdba    false    219            �           2606    24700 #   tarea_comentario estado_tareas_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.tarea_comentario
    ADD CONSTRAINT estado_tareas_pkey PRIMARY KEY (id);
 M   ALTER TABLE ONLY public.tarea_comentario DROP CONSTRAINT estado_tareas_pkey;
       public            laudosdbdba    false    221            �           2606    24702    extracto extracto_numero_unico 
   CONSTRAINT     a   ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_numero_unico UNIQUE (numero_unico);
 H   ALTER TABLE ONLY public.extracto DROP CONSTRAINT extracto_numero_unico;
       public            laudosdbdba    false    223            �           2606    24704    extracto extracto_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT extracto_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.extracto DROP CONSTRAINT extracto_pkey;
       public            laudosdbdba    false    223            �           2606    24706    hojalata hojalata_numero_unico 
   CONSTRAINT     a   ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT hojalata_numero_unico UNIQUE (numero_unico);
 H   ALTER TABLE ONLY public.hojalata DROP CONSTRAINT hojalata_numero_unico;
       public            laudosdbdba    false    225            �           2606    24708    hojalata hojalata_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT hojalata_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.hojalata DROP CONSTRAINT hojalata_pkey;
       public            laudosdbdba    false    225            �           2606    24712    insumo_envase insumo_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT insumo_pkey PRIMARY KEY (id);
 C   ALTER TABLE ONLY public.insumo_envase DROP CONSTRAINT insumo_pkey;
       public            laudosdbdba    false    227            �           2606    24714    mercaderia mercaderia_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT mercaderia_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.mercaderia DROP CONSTRAINT mercaderia_pkey;
       public            laudosdbdba    false    229            �           2606    24716 +   reacondicionado_detalle mezcla_detalle_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT mezcla_detalle_pkey PRIMARY KEY (id);
 U   ALTER TABLE ONLY public.reacondicionado_detalle DROP CONSTRAINT mezcla_detalle_pkey;
       public            laudosdbdba    false    231            �           2606    24718    reacondicionado mezcla_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.reacondicionado
    ADD CONSTRAINT mezcla_pkey PRIMARY KEY (id);
 E   ALTER TABLE ONLY public.reacondicionado DROP CONSTRAINT mezcla_pkey;
       public            laudosdbdba    false    233            �           2606    24720 "   motivo_bloqueo motivo_bloqueo_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT motivo_bloqueo_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.motivo_bloqueo DROP CONSTRAINT motivo_bloqueo_pkey;
       public            laudosdbdba    false    235            �           2606    24722 #   reacondicionado numero_unico_unique 
   CONSTRAINT     f   ALTER TABLE ONLY public.reacondicionado
    ADD CONSTRAINT numero_unico_unique UNIQUE (numero_unico);
 M   ALTER TABLE ONLY public.reacondicionado DROP CONSTRAINT numero_unico_unique;
       public            laudosdbdba    false    233            �           2606    24724    permiso permiso_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT permiso_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.permiso DROP CONSTRAINT permiso_pkey;
       public            laudosdbdba    false    237            �           2606    24726    tarea tareas_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.tarea
    ADD CONSTRAINT tareas_pkey PRIMARY KEY (id);
 ;   ALTER TABLE ONLY public.tarea DROP CONSTRAINT tareas_pkey;
       public            laudosdbdba    false    239            �           2606    24728    ubicacion ubicacion_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT ubicacion_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT ubicacion_pkey;
       public            laudosdbdba    false    241            �           2606    24730 )   ubicacion_nombre ubicaciones_nombres_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.ubicacion_nombre
    ADD CONSTRAINT ubicaciones_nombres_pkey PRIMARY KEY (id);
 S   ALTER TABLE ONLY public.ubicacion_nombre DROP CONSTRAINT ubicaciones_nombres_pkey;
       public            laudosdbdba    false    243            �           2606    24732    mercaderia unique_numero_unico 
   CONSTRAINT     a   ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT unique_numero_unico UNIQUE (numero_unico);
 H   ALTER TABLE ONLY public.mercaderia DROP CONSTRAINT unique_numero_unico;
       public            laudosdbdba    false    229            �           2606    24734    usuario usuario_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public            laudosdbdba    false    245            �           2606    24736    vencimiento vencimiento_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT vencimiento_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.vencimiento DROP CONSTRAINT vencimiento_pkey;
       public            laudosdbdba    false    247                       2606    24737 &   reacondicionado_detalle FK__mercaderia    FK CONSTRAINT     �   ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK__mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);
 R   ALTER TABLE ONLY public.reacondicionado_detalle DROP CONSTRAINT "FK__mercaderia";
       public          laudosdbdba    false    231    3301    229                       2606    24742 "   reacondicionado_detalle FK__mezcla    FK CONSTRAINT     �   ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK__mezcla" FOREIGN KEY (reacondicionado) REFERENCES public.reacondicionado(id);
 N   ALTER TABLE ONLY public.reacondicionado_detalle DROP CONSTRAINT "FK__mezcla";
       public          laudosdbdba    false    231    3307    233                       2606    24747    tarea_comentario FK__tareas    FK CONSTRAINT     z   ALTER TABLE ONLY public.tarea_comentario
    ADD CONSTRAINT "FK__tareas" FOREIGN KEY (tarea) REFERENCES public.tarea(id);
 G   ALTER TABLE ONLY public.tarea_comentario DROP CONSTRAINT "FK__tareas";
       public          laudosdbdba    false    221    3315    239                       2606    24752    tarea FK__usuario    FK CONSTRAINT     x   ALTER TABLE ONLY public.tarea
    ADD CONSTRAINT "FK__usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 =   ALTER TABLE ONLY public.tarea DROP CONSTRAINT "FK__usuario";
       public          laudosdbdba    false    3321    239    245                       2606    24757    tarea_comentario FK__usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.tarea_comentario
    ADD CONSTRAINT "FK__usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 H   ALTER TABLE ONLY public.tarea_comentario DROP CONSTRAINT "FK__usuario";
       public          laudosdbdba    false    221    3321    245                       2606    24762    reacondicionado FK__usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.reacondicionado
    ADD CONSTRAINT "FK__usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 G   ALTER TABLE ONLY public.reacondicionado DROP CONSTRAINT "FK__usuario";
       public          laudosdbdba    false    233    3321    245            �           2606    24767    acceso FK_acceso_usuario    FK CONSTRAINT     {   ALTER TABLE ONLY public.acceso
    ADD CONSTRAINT "FK_acceso_usuario" FOREIGN KEY (usuario) REFERENCES public.usuario(id);
 D   ALTER TABLE ONLY public.acceso DROP CONSTRAINT "FK_acceso_usuario";
       public          laudosdbdba    false    245    3321    215            �           2606    24772    bloqueado FK_bloqueado_extracto    FK CONSTRAINT     �   ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);
 K   ALTER TABLE ONLY public.bloqueado DROP CONSTRAINT "FK_bloqueado_extracto";
       public          laudosdbdba    false    223    217    3293            �           2606    24777    bloqueado FK_bloqueado_hojalata    FK CONSTRAINT     �   ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);
 K   ALTER TABLE ONLY public.bloqueado DROP CONSTRAINT "FK_bloqueado_hojalata";
       public          laudosdbdba    false    225    3297    217            �           2606    24782 !   bloqueado FK_bloqueado_mercaderia    FK CONSTRAINT     �   ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);
 M   ALTER TABLE ONLY public.bloqueado DROP CONSTRAINT "FK_bloqueado_mercaderia";
       public          laudosdbdba    false    3301    217    229                        2606    24787 %   bloqueado FK_bloqueado_motivo_bloqueo    FK CONSTRAINT     �   ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_motivo_bloqueo" FOREIGN KEY (motivo) REFERENCES public.motivo_bloqueo(id);
 Q   ALTER TABLE ONLY public.bloqueado DROP CONSTRAINT "FK_bloqueado_motivo_bloqueo";
       public          laudosdbdba    false    217    235    3311                       2606    24792    bloqueado FK_bloqueado_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.bloqueado
    ADD CONSTRAINT "FK_bloqueado_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 J   ALTER TABLE ONLY public.bloqueado DROP CONSTRAINT "FK_bloqueado_usuario";
       public          laudosdbdba    false    3321    217    245                       2606    24797    despacho FK_despacho_extracto    FK CONSTRAINT     �   ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(id);
 I   ALTER TABLE ONLY public.despacho DROP CONSTRAINT "FK_despacho_extracto";
       public          laudosdbdba    false    219    3293    223                       2606    24802    despacho FK_despacho_hojalata    FK CONSTRAINT     �   ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(id);
 I   ALTER TABLE ONLY public.despacho DROP CONSTRAINT "FK_despacho_hojalata";
       public          laudosdbdba    false    219    3297    225                       2606    24807    despacho FK_despacho_mercaderia    FK CONSTRAINT     �   ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(id);
 K   ALTER TABLE ONLY public.despacho DROP CONSTRAINT "FK_despacho_mercaderia";
       public          laudosdbdba    false    3301    229    219                       2606    24812    despacho FK_despacho_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.despacho
    ADD CONSTRAINT "FK_despacho_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 H   ALTER TABLE ONLY public.despacho DROP CONSTRAINT "FK_despacho_usuario";
       public          laudosdbdba    false    245    219    3321                       2606    24817    extracto FK_extracto_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "FK_extracto_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 H   ALTER TABLE ONLY public.extracto DROP CONSTRAINT "FK_extracto_usuario";
       public          laudosdbdba    false    245    3321    223            	           2606    24822     extracto FK_extracto_vencimiento    FK CONSTRAINT     �   ALTER TABLE ONLY public.extracto
    ADD CONSTRAINT "FK_extracto_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);
 L   ALTER TABLE ONLY public.extracto DROP CONSTRAINT "FK_extracto_vencimiento";
       public          laudosdbdba    false    3323    223    247            
           2606    24827    hojalata FK_hojalata_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT "FK_hojalata_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 H   ALTER TABLE ONLY public.hojalata DROP CONSTRAINT "FK_hojalata_usuario";
       public          laudosdbdba    false    245    3321    225                       2606    24832     hojalata FK_hojalata_vencimiento    FK CONSTRAINT     �   ALTER TABLE ONLY public.hojalata
    ADD CONSTRAINT "FK_hojalata_vencimiento" FOREIGN KEY (vto_meses) REFERENCES public.vencimiento(id);
 L   ALTER TABLE ONLY public.hojalata DROP CONSTRAINT "FK_hojalata_vencimiento";
       public          laudosdbdba    false    247    225    3323                       2606    24837    insumo_envase FK_insumo_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.insumo_envase
    ADD CONSTRAINT "FK_insumo_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 K   ALTER TABLE ONLY public.insumo_envase DROP CONSTRAINT "FK_insumo_usuario";
       public          laudosdbdba    false    3321    245    227                       2606    24842     mercaderia FK_mercaderia_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT "FK_mercaderia_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 L   ALTER TABLE ONLY public.mercaderia DROP CONSTRAINT "FK_mercaderia_usuario";
       public          laudosdbdba    false    229    245    3321                       2606    24847 $   mercaderia FK_mercaderia_vencimiento    FK CONSTRAINT     �   ALTER TABLE ONLY public.mercaderia
    ADD CONSTRAINT "FK_mercaderia_vencimiento" FOREIGN KEY (vto) REFERENCES public.vencimiento(id);
 P   ALTER TABLE ONLY public.mercaderia DROP CONSTRAINT "FK_mercaderia_vencimiento";
       public          laudosdbdba    false    229    3323    247                       2606    24852 8   reacondicionado_detalle FK_mezcla_detalle_mezcla_detalle    FK CONSTRAINT     �   ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK_mezcla_detalle_mezcla_detalle" FOREIGN KEY (reacondicionado_detalle) REFERENCES public.reacondicionado_detalle(id);
 d   ALTER TABLE ONLY public.reacondicionado_detalle DROP CONSTRAINT "FK_mezcla_detalle_mezcla_detalle";
       public          laudosdbdba    false    3305    231    231                       2606    24857 (   motivo_bloqueo FK_motivo_bloqueo_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.motivo_bloqueo
    ADD CONSTRAINT "FK_motivo_bloqueo_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 T   ALTER TABLE ONLY public.motivo_bloqueo DROP CONSTRAINT "FK_motivo_bloqueo_usuario";
       public          laudosdbdba    false    235    245    3321                       2606    24862    permiso FK_permiso_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.permiso
    ADD CONSTRAINT "FK_permiso_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 F   ALTER TABLE ONLY public.permiso DROP CONSTRAINT "FK_permiso_usuario";
       public          laudosdbdba    false    245    237    3321                       2606    24867 =   reacondicionado_detalle FK_reacondicionado_detalle_mercaderia    FK CONSTRAINT     �   ALTER TABLE ONLY public.reacondicionado_detalle
    ADD CONSTRAINT "FK_reacondicionado_detalle_mercaderia" FOREIGN KEY (mercaderia_original) REFERENCES public.mercaderia(id);
 i   ALTER TABLE ONLY public.reacondicionado_detalle DROP CONSTRAINT "FK_reacondicionado_detalle_mercaderia";
       public          laudosdbdba    false    3301    231    229                       2606    24872    ubicacion FK_ubicacion_extracto    FK CONSTRAINT     �   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_extracto" FOREIGN KEY (extracto) REFERENCES public.extracto(numero_unico);
 K   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT "FK_ubicacion_extracto";
       public          laudosdbdba    false    241    3291    223                       2606    24877    ubicacion FK_ubicacion_hojalata    FK CONSTRAINT     �   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_hojalata" FOREIGN KEY (hojalata) REFERENCES public.hojalata(numero_unico);
 K   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT "FK_ubicacion_hojalata";
       public          laudosdbdba    false    241    225    3295                       2606    24887 !   ubicacion FK_ubicacion_mercaderia    FK CONSTRAINT     �   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_mercaderia" FOREIGN KEY (mercaderia) REFERENCES public.mercaderia(numero_unico);
 M   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT "FK_ubicacion_mercaderia";
       public          laudosdbdba    false    3303    241    229                       2606    24892 &   ubicacion FK_ubicacion_reacondicionado    FK CONSTRAINT     �   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_reacondicionado" FOREIGN KEY (reacondicionado) REFERENCES public.reacondicionado(numero_unico);
 R   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT "FK_ubicacion_reacondicionado";
       public          laudosdbdba    false    3309    241    233                       2606    24897 *   ubicacion FK_ubicacion_ubicaciones_nombres    FK CONSTRAINT     �   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_ubicaciones_nombres" FOREIGN KEY (ubicacion_fila) REFERENCES public.ubicacion_nombre(id);
 V   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT "FK_ubicacion_ubicaciones_nombres";
       public          laudosdbdba    false    3319    241    243                       2606    24902    ubicacion FK_ubicacion_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT "FK_ubicacion_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 J   ALTER TABLE ONLY public.ubicacion DROP CONSTRAINT "FK_ubicacion_usuario";
       public          laudosdbdba    false    245    241    3321                       2606    24907 "   vencimiento FK_vencimiento_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.vencimiento
    ADD CONSTRAINT "FK_vencimiento_usuario" FOREIGN KEY (responsable) REFERENCES public.usuario(id);
 N   ALTER TABLE ONLY public.vencimiento DROP CONSTRAINT "FK_vencimiento_usuario";
       public          laudosdbdba    false    247    3321    245            H           826    24981     DEFAULT PRIVILEGES FOR SEQUENCES    DEFAULT ACL     c   ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO laudosdbusr;
          public          postgres    false    4            G           826    24977    DEFAULT PRIVILEGES FOR TABLES    DEFAULT ACL     {   ALTER DEFAULT PRIVILEGES FOR ROLE laudosdbdba IN SCHEMA public GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO laudosdbusr;
          public          laudosdbdba    false    4            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �   �  x���]�� ���*�@���Z��$�'��Qw�ܘ�$uRm�e��y�� ��+UtAqf�L-f�c���hM�6g�Q=q�������pI�a�*~ݐ���2��D�����rѫY��>��T�E��,�o9|;"�U���0ȗ�s�ׇ�0z�,��.�?.��\˂0������RH��es���3��15�n8�ڎ�N2�S���ˉm�ޅ���=�ZQ������bM�)�T^F�L�6Fp�:����}$s7aekg���8�������X a��\Y�a��[��a�q��M���(n�T�L[��i�b�>�|��&\-��f5�O&�-���B(��}�o�\i�����N;��!VXI��\J�x���$F*��.���974��Nd�QK,���J�-y�o��wG):&��Bȇ�@���@^�9#
���A��քҧXC���\�SY�}"���7'8�      �   .  x�u�Yn� �����G�/���9A�bPӄ!/��<�c���4�1�X�ECn�ҁr�����<�]7�����Bl��8E�O)[)���a�)�ԭ�� R�C�v��H�	T8FK�Vt�ߢ��b���d/��ҫ�?K����ƈ��vM�����ꅝ�s6p5�9f��5�ń�TsX�[[�ycD����|}�و ܱl��׍�V� �T�ako��RCm萪�#+�W�ǫ�{��ZSf�kdo��X�bl���C�V�9��������V�)ui��
���r+�Bj_Q�����M�      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �   5  x����n������4���}��[0�[�[t߾��R,�3�;�o$}�:�����˿�x~�������緗׷-Z�J�Z֣د"��񋌡]����?�x����Q������<?�㟏����Z�����V�����Y�ûno���F�������ߟ�ߞ>t�""�p��{����������������!�pp����O�㏏��l�P'�^�����]E{���zx{��_>E23�Nc)a��Z�iXKX���Nc�J��հ��n�z�r.�԰��ڬ������zJ�����̺�8�a�����7��0����N�DIY6a�`)f����T�J��!�+p
��k��u�
��n�W T(�!e�� *�j�2@*��=^
T�T������l�1S@U
uz4�3e�J�.)��T�J��*���R�k�H-�ʠZ���e7@U�J�xM�=���ۓg�HꟘ���z�+7_�beF�5c�a^��E<�
�ƭ��s,��y�泬sa�������M�jXOj���ΡW����S�i^�p��Vl�	�Sծ�U�X�e��U�Xu����*���-�RV8Y�j4J���Z��݀V8[�+������\r����p�Ճ!�W9�*�^�x�@�}��om%����r�57�����բ�h૜o��Y	��r��"{w�U�wT*x���F������.��8�Yg��x��C`���Υ3ƓI��]2"|:�ǻ��(܁�8^_N=��ǻ����k��#v��F��R~|���+�s��VʷB�N��R��V��|+�[˴������Ï��K�V��� �J�V�s��?��R�U�8���R�U<��������#�&�V�W���}�m����v1��q�շߓ����������8��[�&�6η�9/�'�*η�y����6[�������%�i�|?<j�L�x���k�3=,���w�z�^x�p{�n�v������n�~�<q-��ڏ"���q�C�	�"��*�����f8�p���]C[(`�9�� yp��8z�(J����'G8P̭�kjJ�A9{������j9$��t�2b@i�AI{]��X$I�t�3X�Y zP�MV�= zP�M�
 zRо�VU zr��� =9h�5Ν~���xĞ �䠭`C��A�q������%�(@Oں�+�bNګ���'']=��*)H/Nڧe�(H/N�Z�H/N��ޜH/N�s1bIAzq�^)/<�'�$��@zq��Oӑ4�'�<1��I�>BeK�n���	[���2���H�=\5H��u�Eԣ��g�
R8�>���S)�(� #���y�ɨě�*ױQ��x�S�:6$��Y?ŮcG�Spϐzױ%1�Y
v�-y	g�O��S��̧�L�!�G��m�K8��uG�F[�N|���l�K8�%�ζ�%������p����H�������	罖6�%o��{��̖*�(�݋ o[���q��_*a��x/g?I-L�����4M5L��ū�U�a�y�BROIL�"�]�}\"W��������(E�e�����G��WɒʘG�j�i$r���w}�j����f�ȍ#�1�S!��uɈ��F&Ƒ[�w���8r��#�Gn~.��J�L�37�*/�2����9��+gnה�z�T�܆�H%��I��m^���48s�%I�fR9�Zjt}H�fR9s?�`L�L*g^=%��S;�ʙ��qɼr�>�ݩ�I���X�Q%�ƙ�i��I�̛B%�TѤq��g��M�3o;����ې��$�4i��Q��C"o���q�()�	��z��	䩨	��z?n��#�sQ����x"�Z��Q�j�u�ާ��G��Z�k�!����q�S�{yjk���g�>EC�w��{xb@�IOy�3�h��$�5I}�3�5ы��������19�$�
�gj�Q%��>�iZSb���>�`�<E��<���Q%���OOpxF2��U�#e6���D���k�|t��&�#_�K&M�MG��!tSj�ɑ���)M�M&G�f�,�)����ך��i�m2)�Q${�Rn�I�����|R�÷�hl��dR��T�dR䣬՘�nS��}�Y�J�2��:?4E7Y�����H�"�D�A%�E�m{�n�8rC>#�/���6�/N�AGO���&�W��ISx�Ł{�{���&��a�`���\WN�vo
ne)��)�7?���TV8�6&:S{��R&�=*��4�zR{���+ M�MG�=�D�fjoZ8�*v��޴p��M�ٮR8sw(�ڛ
g>��3vGg>F��H��9�𯩾�p�h��&s�̧W��y2��k�4�7��g+j�o*��%ڟ4�7�|��BS~S��=ƉKw�r��а��	mw�=~}�������'7�c5�x�yw��m��@��i�?��y5Tk�Wm7�]9�"�.�s���\�v6��$�]l���ڹY:g�즶k����np�n�����v��n��~�EM�Ow�۵���)�����Uk�~jwl��M1���x7����'�j��� ;�y�s��0O
�JS#T�`�$���n�g��0�`^Qb�IQ�v���8�k�Zo�W*_d����E�3�������VoG���(��n�M��yf�OR�y�\K	�IS�ԭH^;K;�I��䵳MTөS��)����p�ے�s+x#S��-^^�*>%��1u���u"�R��-i^;wT�)n�7�}W���sj�_�Kp޽ݷ�{��a����v|�w�W*��n�Wo5.j5EQm����䌯v;��ޜS*�~;��-�3US���{|a�`�v���WSL�~;�< ����[X�v���ۜ�n��ڹJ��Xٟ���-���«n���w���-5X�������r�n9���Pf��Tfu+���^��Y)��i���u�9l���~ð3��t{��G�� ����sظ`�;�]�lI�d�r;¼N�+bK�W��[M��6nG��	K!X��[y�g�	�a��%�3���[E (X*�:�F�*^��9#lލ�UZ���˗/�P!e      �   �  x����n� ���)�A��ӳ�8�֕m"C.�O��&�6@U��G��'��H���0�qO���R�<
{�*�����pw��Z�"��o��#��܁��́p�<���PMΗq�s���g=�f�+#��'Z(�!n�i�פu��^��\�����2�8~��֦wL�9tl-Ԓ%�[a>��A ˤ�Jˎ���:rb.[ڳ5� � ҩ����
2��6�5�!-q-8���#�A�J����/鏴PO�8ca�I�Q���1�5.k7ZS�('�S��Ӻg�����|GYQT
����ϡ'S�)���/{�(��uN���g��N�k�BE����]�G#�6 0'@�k�BMr����l�.Hɼ�S��tMQ	d��[�➍�+l.�E�U���,y����l��vV�k';�����g8��!�{�J��,c:m���t�5OKZ�Rҷi%�c{uLzaeS������\���5�Y���,�9��h+Z����1�c(      �   �   x�}�;�0�z}
.�h?^{7=}
JR E�8>��q�4����k+�����>�M���)�(Aa.OEI;�PS�	�e-��~��e��f���t(�f��~t[�lWs����/˪�#��:U�Q�ԩ�+1�s��Ñ��c�1��{3Nm     