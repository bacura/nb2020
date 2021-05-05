//guild.js ver 0.01b

/////////////////////////////////////////////////////////////////////////////////
// Koyomi //////////////////////////////////////////////////////////////

// Koyomi
var initKoyomi = function(){
	$.post( "koyomi.cgi", { command:"menu" }, function( data ){ $( "#LINE" ).html( data );});
	$.post( "koyomi.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
	flashBW();
	dl1 = true;
	displayBW();
	displayLINE( 'on');
};

// Koyomi change
var changeKoyomi = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "koyomi.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};

// Koyomi freeze
var freezeKoyomi = function( dd ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var freeze_check = document.getElementById( "freeze_check" + dd ).checked ;
	$.post( "koyomi.cgi", { command:'freeze', yyyy_mm:yyyy_mm, dd, freeze_check:freeze_check }, function( data ){ $( "#L1" ).html( data );});
};

// Koyomi freeze all
var freezeKoyomiAll = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var freeze_check_all = document.getElementById( "freeze_check_all" ).checked ;
	$.post( "koyomi.cgi", { command:'freeze_all', yyyy_mm:yyyy_mm,  freeze_check_all:freeze_check_all }, function( data ){ $( "#L1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi Edit//////////////////////////////////////////////////////////////

// Koyomi edit
var editKoyomi = function( com, dd ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "koyomi-edit.cgi", { command:com, yyyy_mm:yyyy_mm, dd:dd }, function( data ){ $( "#L2" ).html( data );});
	flashBW();
	dl2 = true;
	displayBW();
};

// Koyomi delete
var deleteKoyomi = function( yyyy, mm, dd, tdiv, code, order ){
	$.post( "koyomi-edit.cgi", { command:'delete', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, code:code, order:order }, function( data ){ $( "#L2" ).html( data );});
};

// Koyomi memo
var memoKoyomi = function( yyyy, mm, dd ){
	var memo = document.getElementById( "memo" ).value;
	$.post( "koyomi-edit.cgi", { command:'memo', yyyy:yyyy, mm:mm, dd:dd, memo:memo }, function( data ){ $( "#L2" ).html( data );});
	displayVIDEO( 'memo saved');
};

// Koyomi Save Something
var koyomiSaveSome = function( yyyy, mm, dd, tdiv, id ){
	var some = document.getElementById( id ).value;
	$.post( "koyomi-edit.cgi", { command:'some', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:99, some:some }, function( data ){ $( "#L2" ).html( data );});
	displayVIDEO( 'Something saved' );
};

// Koyomi edit return
var editKoyomiR = function( yyyy, mm ){
	$.post( "koyomi.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){ $( "#L1" ).html( data );});
	dl1 = true;
	dl2 = false;
	displayBW();
};


// レシピ編集の写真をアップロードして保存、そしてL3に写真を再表示
var koyomiPhotoSave = function( code, form, dd ){
	form_data = new FormData( $( form )[0] );
	form_data.append( 'command', 'upload' );
	form_data.append( 'code', code );
	form_data.append( 'base', 'koyomi' );
	$.ajax( "photo.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ setTimeout( editKoyomi( 'init', dd ), 2000); }
		}
	);
};


// delete photo from media db
var koyomiPhotoDel = function( code, mcode, dd ){
	$.post( "photo.cgi", { command:'delete', code:code, mcode:mcode, base:'koyomi' }, function( data ){});
	setTimeout( editKoyomi( 'init', dd ), 2000);
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi calc //////////////////////////////////////////////////////////////

// Koyomi calc
var calcKoyomi = function( yyyy, mm, dd, palette ){
	if( palette ){
		var palette = document.getElementById( "palette" ).value;
	}

	document.getElementById( "L1" ).style.display = 'none';
	$.post( "koyomi-calc.cgi", { command:"init", yyyy:yyyy, mm:mm, dd:dd, palette:palette }, function( data ){ $( "#L2" ).html( data );});
	dl1 = false;
	dl2 = true;
	displayBW();
};

// Koyomi calc return
var calcKoyomiR = function( yyyy, mm ){
	dl1 = true;
	dl2 = false;
	displayBW();
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi Direct fix data //////////////////////////////////////////////////////////////

// Koyomi fix
var fixKoyomi = function( com, yyyy, mm, dd, tdiv ){
	$.post( "koyomi-fix.cgi", { command:com, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv }, function( data ){ $( "#L3" ).html( data );});
	dl3 = true;
	displayBW();
};

// Koyomi fix
var paletteKoyomi = function( yyyy, mm, dd, tdiv, modifyf ){
	displayVIDEO( modifyf );
	var palette = document.getElementById( "palette" ).value;
	$.post( "koyomi-fix.cgi", { command:'palette', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, palette:palette, modifyf:modifyf }, function( data ){ $( "#L3" ).html( data );});
};

// Koyomi fix 100g check
var koyomiG100check = function(){
	if(document.getElementById( "g100_check" ).checked){
		document.getElementById( "food_weight" ).disabled = false;
	}else{
		document.getElementById( "food_weight" ).disabled = true;
	}
};


// Koyomi fix save
var koyomiSaveFix = function( yyyy, mm, dd, tdiv, modifyf, order ){
	var food_name = document.getElementById( "food_name" ).value;
	var hh = document.getElementById( "hh_fix" ).value;
	var food_number = document.getElementById( "food_number" ).value;

	if( food_name != '' ){
		if(document.getElementById( "g100_check" ).checked){
			var food_weight = document.getElementById( "food_weight" ).value;
		}else{
			var food_weight = 100;
		}
		var ENERC = document.getElementById( "ENERC" ).value;
		var ENERC_KCAL = document.getElementById( "ENERC_KCAL" ).value;
		var WATER = document.getElementById( "WATER" ).value;

		var PROTCAA = document.getElementById( "PROTCAA" ).value;
		var PROT = document.getElementById( "PROT" ).value;
		var FATNLEA = document.getElementById( "FATNLEA" ).value;
		var CHOLE = document.getElementById( "CHOLE" ).value;
		var FAT = document.getElementById( "FAT" ).value;
		var CHOAVLM = document.getElementById( "CHOAVLM" ).value;
		var CHOAVL = document.getElementById( "CHOAVL" ).value;
		var CHOAVLMF = document.getElementById( "CHOAVLMF" ).value;
		var FIB = document.getElementById( "FIB" ).value;
		var POLYL = document.getElementById( "POLYL" ).value;
		var CHOCDF = document.getElementById( "CHOCDF" ).value;
		var OA = document.getElementById( "OA" ).value;

		var ASH = document.getElementById( "ASH" ).value;
		var NA = document.getElementById( "NA" ).value;
		var K = document.getElementById( "K" ).value;
		var CA = document.getElementById( "CA" ).value;
		var MG = document.getElementById( "MG" ).value;
		var P = document.getElementById( "P" ).value;
		var FE = document.getElementById( "FE" ).value;
		var ZN = document.getElementById( "ZN" ).value;
		var CU = document.getElementById( "CU" ).value;
		var MN = document.getElementById( "MN" ).value;
		var ID = document.getElementById( "ID" ).value;
		var SE = document.getElementById( "SE" ).value;
		var CR = document.getElementById( "CR" ).value;
		var MO = document.getElementById( "MO" ).value;

		var RETOL = document.getElementById( "RETOL" ).value;
		var CARTA = document.getElementById( "CARTA" ).value;
		var CARTB = document.getElementById( "CARTB" ).value;
		var CRYPXB = document.getElementById( "CRYPXB" ).value;
		var CARTBEQ = document.getElementById( "CARTBEQ" ).value;
		var VITA_RAE = document.getElementById( "VITA_RAE" ).value;
		var VITD = document.getElementById( "VITD" ).value;
		var TOCPHA = document.getElementById( "TOCPHA" ).value;
		var TOCPHB = document.getElementById( "TOCPHB" ).value;
		var TOCPHG = document.getElementById( "TOCPHG" ).value;
		var TOCPHD = document.getElementById( "TOCPHD" ).value;
		var VITK = document.getElementById( "VITK" ).value;

		var THIAHCL = document.getElementById( "THIAHCL" ).value;
		var RIBF = document.getElementById( "RIBF" ).value;
		var NIA = document.getElementById( "NIA" ).value;
		var NE = document.getElementById( "NE" ).value;
		var VITB6A = document.getElementById( "VITB6A" ).value;
		var VITB12 = document.getElementById( "VITB12" ).value;
		var FOL = document.getElementById( "FOL" ).value;
		var PANTAC = document.getElementById( "PANTAC" ).value;
		var BIOT = document.getElementById( "BIOT" ).value;
		var VITC = document.getElementById( "VITC" ).value;

		var ALC = document.getElementById( "ALC" ).value;
		var NACL_EQ = document.getElementById( "NACL_EQ" ).value;

		$.post( "koyomi-fix.cgi", {
			command:'save', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh,
			food_name:food_name, food_weight:food_weight, food_number:food_number, modifyf:modifyf, order:order,
			ENERC:ENERC, ENERC_KCAL:ENERC_KCAL, WATER:WATER,
			PROTCAA:PROTCAA, PROT:PROT, FATNLEA:FATNLEA, CHOLE:CHOLE, FAT:FAT, CHOAVLM:CHOAVLM, CHOAVL:CHOAVL, CHOAVLMF:CHOAVLMF, CHOCDF:CHOCDF, OA:OA,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIAHCL:THIAHCL, RIBF:RIBF, NIA:NIA, NE:NE, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			ALC:ALC, NACL_EQ:NACL_EQ
		}, function( data ){ $( "#L3" ).html( data );});

		displayVIDEO( food_name + ' saved' );

		var fx = function(){
			$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#L2" ).html( data );});
		};
		setTimeout( fx , 1000 );
	} else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};


// Koyomi modify or copy panel fix
var modifyKoyomif = function( code, yyyy, mm, dd, tdiv, hh, order ){
	$.post( "koyomi-fix.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, order:order }, function( data ){ $( "#L3" ).html( data );});
	dl3 = true;
	displayBW();
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi import panel//////////////////////////////////////////////////////////////

// Koyomi insert panel
var addKoyomi = function( code ){
	$.post( "koyomi-add.cgi", { command:"init", code:code }, function( data ){ $( "#LF" ).html( data );});
	pushBW();
	flashBW();
	dlf = true;
	displayBW();
	displayLINE( 'off' );
};

// Koyomi insert panel change
var changeKoyomiAdd = function( com, code, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	$.post( "koyomi-add.cgi", { command:com, code:code, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

// Updating code into Koyomi
var saveKoyomiAdd = function( com, code, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var copy = 0;
	if( document.getElementById( "copy" )){
		if( document.getElementById( "copy" ).checked ){ copy = 1; }
	}
	$.post( "koyomi-add.cgi", { command:com, code:code, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin, copy:copy }, function( data ){ $( "#LF" ).html( data );});
};

// Saving code into Koyomi direct
var saveKoyomiAdd_direct = function( code, yyyy, mm, dd, tdiv, origin ){
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	$.post( "koyomi-add.cgi", { command:"save", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

// Modifying or copying code in Koyomi
var modifysaveKoyomi_direct = function( code, yyyy, mm, dd, tdiv, origin ){
	var hh = document.getElementById( "hh" ).value;
	var copy = 0;
	if( document.getElementById( "copy" ).checked ){ copy = 1; }
	$.post( "koyomi-add.cgi", { command:"move", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, origin:origin, copy:copy }, function( data ){ $( "#LF" ).html( data );});
};

// Modifying or copying fix code in Koyomi
var modifysaveKoyomiFC = function( code, origin ){
	$.post( "koyomi-add.cgi", { command:"move_fix", code:code, origin:origin, copy:1 }, function( data ){ $( "#LF" ).html( data );});
	ldf = true;
	displayBW();
};

// Return from Koyomi
var koyomiReturn = function(){
	pullHW();
	displayBW();
};

// Return from Koyomi to Koyomi edit
var koyomiReturn2KE = function( yyyy, mm, dd ){
	$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#L2" ).html( data );});
	pullHW();
	displayBW();
};

// Koyomi modify or copy panel
var modifyKoyomi = function( code, yyyy, mm, dd, tdiv, hh, ev, eu, order ){
	$.post( "koyomi-add.cgi", {command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, order:order }, function( data ){ $( "#LF" ).html( data );});
	ldf = true;
	displayBW();
};

// Koyomi insert panel change  for fix code
var modifychangeKoyomiFC = function( code, origin ){
	var hh = document.getElementById( "hh" ).value;
	displayVIDEO( mm );
	$.post( "koyomi-add.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#LF" ).html( data );});
	ldf = true;
	displayBW();
};

// Set time to now
var nowKoyomi = function(){
	var today = new Date();
	var hh = today.getHours();
	document.getElementById( 'hh' ).value = hh;
};

/////////////////////////////////////////////////////////////////////////////////
// Koyomi menu copy / move //////////////////////////////////////////////////////////////

var cmmKoyomi = function( cm_mode, yyyy, mm, dd, tdiv ){
	$.post( "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:99 }, function( data ){ $( "#LF" ).html( data );});
	pushBW();
	flashBW();
	dlf = true;
	displayBW();
};

var cmmChangeKoyomi = function( cm_mode, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv_cmm" ).value;
	var hh = document.getElementById( "hh_cmm" ).value;
	$.post( "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh:hh, origin:origin }, function( data ){ $( "#LF" ).html( data );});
	document.getElementById( "LF" ).style.display = 'block';
};

var cmmSaveKoyomi = function( cm_mode, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv_cmm" ).value;
	var hh = document.getElementById( "hh_cmm" ).value;

	$.post( "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh:hh, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

var cmmSaveKoyomi_direct = function( cm_mode, yyyy, mm, dd, tdiv, origin ){
	var hh = document.getElementById( "hh_cmm" ).value;
	$.post( "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

// Set time to now
var cmmNowKoyomi = function(){
	var today = new Date();
	var hh = today.getHours();
	document.getElementById( 'hh_cmm' ).value = hh;
};

/////////////////////////////////////////////////////////////////////////////////
// Koyomi EX //////////////////////////////////////////////////////////////

// Koyomi EX init
var initKoyomiex = function(){
	$.post( "koyomiex.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
};

// Koyomi EX change
var changeKoyomiex = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "koyomiex.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};

// Updating Koyomiex cell
var updateKoyomiex = function( dd, item_no, cell_id ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var cell = document.getElementById( cell_id ).value;
//	$.post( "koyomiex.cgi", { command:"update", yyyy:yyyy, mm:mm, dd:dd, item_no:item_no, cell:cell }, function( data ){ $( "#L1" ).html( data );});
	$.post( "koyomiex.cgi", { command:"update", yyyy_mm:yyyy_mm, dd:dd, item_no:item_no, cell:cell }, function( data ){});
};


/////////////////////////////////////////////////////////////////////////////////
// Ginmi //////////////////////////////////////////////////////////////

// Ginmi init
var initGinmi = function(){
	closeBroseWindows( 1 );
	$.post( "ginmi.cgi", { mod:'line' }, function( data ){ $( "#LINE" ).html( data );});
	displayLINE( 'on' );
	$.post( "ginmi.cgi", { mod:'' }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};

var ginmiForm = function( mod ){
	$.post( "ginmi.cgi", { mod:mod, command:'form' }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Tokei R //////////////////////////////////////////////////////////////

// Tokei R init
var initToker = function(){
	closeBroseWindows( 1 );
	$.post( "toker.cgi", { mod:'line' }, function( data ){ $( "#LINE" ).html( data );});
	displayLINE( 'on');

	$.post( "toker.cgi", { mod:'' }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};

var tokerForm = function( mod ){
	$.post( "toker.cgi", { mod:mod, command:'form' }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};
