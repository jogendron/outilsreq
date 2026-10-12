create schema donnees_ouvertes;

create table donnees_ouvertes.domaine_valeur (
	typ_dom_val 			varchar(50) not null,
	cod_dom_val 			varchar(25) not null,
	val_dom_fran 			varchar(500),
	primary key (typ_dom_val, cod_dom_val)
);

create table donnees_ouvertes.entreprise (
	neq 					varchar(10) not null primary key,
	ind_fail 				boolean,
	dat_immat				date,
	cod_regim_juri			varchar(25),
	cod_intval_emplo_que	varchar(25),
	dat_cess_prevu			date,
	cod_stat_immat			varchar(25),
	cod_forme_juri			varchar(25),
	dat_stat_immat			date,
	cod_regim_juri_consti	varchar(25),
	dat_depo_declr			date,
	an_decl					integer,
	an_prod					integer,
	dat_limit_prod			date,
	an_prod_pre				integer,
	dat_limit_prod_pre		date,
	dat_maj_index_nom		date,
	cod_act_econ_cae		varchar(25),
	no_act_econ_assuj		integer,
	desc_act_econ_assuj		varchar(300),
	cod_act_econ_cae2		varchar(25),
	no_act_econ_assuj2		integer,
	desc_act_econ_assuj2	varchar(300),
	nom_loclt_consti		varchar(100),
	dat_consti				date,
	ind_conven_unmn_actnr	boolean,
	ind_ret_tout_pouvr		boolean,
	ind_limit_resp			boolean,
	dat_deb_resp			date,
	dat_fin_resp			date,
	objet_soc				varchar(1000),
	no_mtr_volont			varchar(10),
	adr_domcl_adr_disp		boolean,
	adr_domcl_lign1_adr		varchar(100),
	adr_domcl_lign2_adr		varchar(100),
	adr_domcl_lign3_adr		varchar(100),
	adr_domcl_lign4_adr		varchar(100)
);

create table donnees_ouvertes.nom (
	neq						varchar(10) not null references donnees_ouvertes.entreprise(neq),
	nom_assuj				varchar(500),
	nom_assuj_lang_etrng	varchar(500),
	stat_nom				varchar(25),
	typ_nom_assuj			varchar(25),
	dat_init_nom_assuj		date,
	dat_fin_nom_assuj		date,
	primary key	(neq, nom_assuj, stat_nom, typ_nom_assuj)
);

create table donnees_ouvertes.etablissement(
	neq						varchar(10) not null references donnees_ouvertes.entreprise(neq),
	no_suf_etab				integer,
	ind_etab_princ			boolean,
	ind_salon_bronz			boolean,
	ind_vente_tabac_detl	boolean,
	ind_disp				boolean,
	lign1_adr				varchar(100),
	lign2_adr				varchar(100),
	lign3_adr				varchar(100),
	lign4_adr				varchar(100),
	cod_act_econ			varchar(25),
	desc_act_econ_etab		varchar(500),
	no_act_econ_etab		integer,
	cod_act_econ2			varchar(25),
	desc_act_econ_etab2		varchar(500),
	no_act_econ_etab2		integer,
	nom_etab				varchar(500),
	primary key (neq, no_suf_etab)
);

create table donnees_ouvertes.fusion_scission(
	neq						varchar(10) not null references donnees_ouvertes.entreprise(neq),
	neq_assuj_rel			varchar(10) references donnees_ouvertes.entreprise(neq),
	denomn_soc				varchar(500),
	cod_rela_assuj			varchar(25),
	dat_efctvt				date,
	ind_disp				boolean,
	lign1_adr				varchar(100),
	lign2_adr				varchar(100),
	lign3_adr				varchar(100),
	lign4_adr				varchar(100),
	primary key (neq, neq_assuj_rel, cod_rela_assuj, dat_efctvt)
);

create table donnees_ouvertes.continuation_transformation(
	neq						varchar(10) not null references donnees_ouvertes.entreprise(neq),
	cod_typ_chang			varchar(25),
	cod_regim_juri			varchar(25),
	autr_regim_juri			varchar(100),
	nom_loclt				varchar(100),
	dat_efctvt				date,
	primary key (neq, cod_typ_chang, dat_efctvt)
);