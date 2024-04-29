//guild.js ver 0.42b (2024/04/20)

kp = 'koyomi/'

/////////////////////////////////////////////////////////////////////////////////
// Koyomi //////////////////////////////////////////////////////////////

// Koyomi
var initKoyomi = function(){
	$.post( kp + "koyomi.cgi", { command:"menu" }, function( data ){ $( "#LINE" ).html( data );});
	$.post( kp + "koyomi.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data ); });

	flashBW();
	dl1 = true;
	dline = true;
	displayBW();
};

// Koyomi change
var changeKoyomi = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( kp + "koyomi.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};

// Koyomi freeze
var freezeKoyomi = function( dd ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var freeze_check = document.getElementById( "freeze_check" + dd ).checked ;
	$.post( kp + "koyomi.cgi", { command:'freeze', yyyy_mm:yyyy_mm, dd, freeze_check:freeze_check }, function( data ){ $( "#L1" ).html( data );});
};

// Koyomi freeze all
var freezeKoyomiAll = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var freeze_check_all = document.getElementById( "freeze_check_all" ).checked ;
	$.post( kp + "koyomi.cgi", { command:'freeze_all', yyyy_mm:yyyy_mm,  freeze_check_all:freeze_check_all }, function( data ){ $( "#L1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi Edit//////////////////////////////////////////////////////////////

// Koyomi edit
const editKoyomi = function( com, dd ){
	const yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( kp + "koyomi-edit.cgi", { command:com, yyyy_mm:yyyy_mm, dd:dd }, function( data ){
		$( "#L2" ).html( data );
		flashBW();
		dl2 = true;
		dline = true;
		displayBW();
	});
};

// Koyomi edit 2 with yy_mm_dd
const editKoyomi2 = function( com, dd ){
	const yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	$.post( kp + "koyomi-edit.cgi", { command:com, yyyy_mm_dd:yyyy_mm_dd, dd:dd }, function( data ){
		$( "#L2" ).html( data );
		flashBW();
		dl2 = true;
		dline = true;
		displayBW();
	});
};

// Koyomi delete
const deleteKoyomi = function( yyyy, mm, dd, tdiv, code, order ){
	$.post( kp + "koyomi-edit.cgi", { command:'delete', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, code:code, order:order }, function( data ){ $( "#L2" ).html( data );});
};

// Koyomi memo
const memoKoyomi = function( yyyy, mm, dd ){
	const memo = document.getElementById( "memo" ).value;
	if( document.getElementById( "bind2n" ).checked ){ var bind2n = 1; }else{ var bind2n = 0; };
	$.post( kp + "koyomi-edit.cgi", { command:'memo', yyyy:yyyy, mm:mm, dd:dd, memo:memo, bind2n:bind2n }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'memo saved');
	});
};

// Koyomi Save Something
const koyomiSaveSome = function( yyyy, mm, dd, tdiv, id ){
	const some = document.getElementById( id ).value;
	$.post( kp + "koyomi-edit.cgi", { command:'some', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:99, some:some }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Something saved' );
	});
};

// Koyomi clear
const clearKoyomi = function( yyyy, mm, dd ){
	if( document.getElementById( 'check_kc' ).checked ){
		$.post( kp + "koyomi-edit.cgi", { command:'clear', yyyy:yyyy, mm:mm, dd:dd }, function( data ){
			$( "#L2" ).html( data );
			displayVIDEO( 'Cleared' );
		});
	}else{
		displayVIDEO( '(>_<)check!' );
	}
};

// Koyomi edit return
const editKoyomiR = function( yyyy, mm ){
	$.post( kp + "koyomi.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		dl2 = false;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi Direct fix data //////////////////////////////////////////////////////////////

// Koyomi fix
var fixKoyomi = function( com, yyyy, mm, dd, tdiv ){
	$.post( kp + "koyomi-fix.cgi", { command:com, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv }, function( data ){
		$( "#L3" ).html( data );

		dl2 = false;
		dl3 = true;
		displayBW();
	});
};

// Koyomi fix
var paletteKoyomi = function( yyyy, mm, dd, tdiv, modifyf ){
	displayVIDEO( modifyf );
	var palette = document.getElementById( "palette" ).value;
	$.post( kp + "koyomi-fix.cgi", { command:'palette', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, palette:palette, modifyf:modifyf }, function( data ){ $( "#L3" ).html( data );});
};

// Koyomi fix 100g check
var koyomiG100check = function(){
	if(document.getElementById( "g100_check" ).checked){
		document.getElementById( "kffood_weight" ).disabled = false;
	}else{
		document.getElementById( "kffood_weight" ).disabled = true;
	}
};


// Koyomi fix save
var koyomiSaveFix = function( yyyy, mm, dd, tdiv, modifyf, order ){
	var food_name = document.getElementById( "food_name" ).value;
	var hh_mm = document.getElementById( "hh_mm_fix" ).value;
	var meal_time = document.getElementById( "meal_time_fix" ).value;
	var food_number = document.getElementById( "food_number" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }

	if( food_name != '' ){
		if(document.getElementById( "g100_check" ).checked){
			var food_weight = document.getElementById( "kffood_weight" ).value;
		}else{
			var food_weight = 100;
		}
		var ENERC = document.getElementById( "kfENERC" ).value;
		var ENERC_KCAL = document.getElementById( "kfENERC_KCAL" ).value;
		var WATER = document.getElementById( "kfWATER" ).value;

		var PROTCAA = document.getElementById( "kfPROTCAA" ).value;
		var PROT = document.getElementById( "kfPROT" ).value;
		var PROTV = document.getElementById( "kfPROTV" ).value;
		var FATNLEA = document.getElementById( "kfFATNLEA" ).value;
		var CHOLE = document.getElementById( "kfCHOLE" ).value;
		var FAT = document.getElementById( "kfFAT" ).value;
		var FATV = document.getElementById( "kfFATV" ).value;
		var CHOAVLM = document.getElementById( "kfCHOAVLM" ).value;
		var CHOAVL = document.getElementById( "kfCHOAVL" ).value;
		var CHOAVLDF = document.getElementById( "kfCHOAVLDF" ).value;
		var CHOV = document.getElementById( "kfCHOV" ).value;
		var FIB = document.getElementById( "kfFIB" ).value;
		var POLYL = document.getElementById( "kfPOLYL" ).value;
		var CHOCDF = document.getElementById( "kfCHOCDF" ).value;
		var OA = document.getElementById( "kfOA" ).value;

		var ASH = document.getElementById( "kfASH" ).value;
		var NA = document.getElementById( "kfNA" ).value;
		var K = document.getElementById( "kfK" ).value;
		var CA = document.getElementById( "kfCA" ).value;
		var MG = document.getElementById( "kfMG" ).value;
		var P = document.getElementById( "kfP" ).value;
		var FE = document.getElementById( "kfFE" ).value;
		var ZN = document.getElementById( "kfZN" ).value;
		var CU = document.getElementById( "kfCU" ).value;
		var MN = document.getElementById( "kfMN" ).value;
		var ID = document.getElementById( "kfID" ).value;
		var SE = document.getElementById( "kfSE" ).value;
		var CR = document.getElementById( "kfCR" ).value;
		var MO = document.getElementById( "kfMO" ).value;

		var RETOL = document.getElementById( "kfRETOL" ).value;
		var CARTA = document.getElementById( "kfCARTA" ).value;
		var CARTB = document.getElementById( "kfCARTB" ).value;
		var CRYPXB = document.getElementById( "kfCRYPXB" ).value;
		var CARTBEQ = document.getElementById( "kfCARTBEQ" ).value;
		var VITA_RAE = document.getElementById( "kfVITA_RAE" ).value;
		var VITD = document.getElementById( "kfVITD" ).value;
		var TOCPHA = document.getElementById( "kfTOCPHA" ).value;
		var TOCPHB = document.getElementById( "kfTOCPHB" ).value;
		var TOCPHG = document.getElementById( "kfTOCPHG" ).value;
		var TOCPHD = document.getElementById( "kfTOCPHD" ).value;
		var VITK = document.getElementById( "kfVITK" ).value;

		var THIA = document.getElementById( "kfTHIA" ).value;
		var RIBF = document.getElementById( "kfRIBF" ).value;
		var NIA = document.getElementById( "kfNIA" ).value;
		var NE = document.getElementById( "kfNE" ).value;
		var VITB6A = document.getElementById( "kfVITB6A" ).value;
		var VITB12 = document.getElementById( "kfVITB12" ).value;
		var FOL = document.getElementById( "kfFOL" ).value;
		var PANTAC = document.getElementById( "kfPANTAC" ).value;
		var BIOT = document.getElementById( "kfBIOT" ).value;
		var VITC = document.getElementById( "kfVITC" ).value;

		var ALC = document.getElementById( "kfALC" ).value;
		var NACL_EQ = document.getElementById( "kfNACL_EQ" ).value;

		var FASAT = document.getElementById( "kfFASAT" ).value;
		var FAMS = document.getElementById( "kfFAMS" ).value;
		var FAPU = document.getElementById( "kfFAPU" ).value;
		var FAPUN3 = document.getElementById( "kfFAPUN3" ).value;
		var FAPUN6 = document.getElementById( "kfFAPUN6" ).value;

		var FIBTG = document.getElementById( "kfFIBTG" ).value;
		var FIBSOL = document.getElementById( "kfFIBSOL" ).value;
		var FIBINS = document.getElementById( "kfFIBINS" ).value;
		var FIBTDF = document.getElementById( "kfFIBTDF" ).value;
		var FIBSDFS = document.getElementById( "kfFIBSDFS" ).value;
		var FIBSDFP = document.getElementById( "kfFIBSDFP" ).value;
		var FIBIDF = document.getElementById( "kfFIBIDF" ).value;
		var STARES = document.getElementById( "kfSTARES" ).value;

		$.post( kp + "koyomi-fix.cgi", {
			command:'save', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time,meal_time,
			food_name:food_name, food_weight:food_weight, food_number:food_number, modifyf:modifyf, carry_on:carry_on, order:order,
			ENERC:ENERC, ENERC_KCAL:ENERC_KCAL, WATER:WATER,
			PROTCAA:PROTCAA, PROT:PROT, PROTV:PROTV, FATNLEA:FATNLEA, CHOLE:CHOLE, FAT:FAT, FATV:FATV, CHOAVLM:CHOAVLM, CHOAVL:CHOAVL, CHOAVLDF:CHOAVLDF, CHOV:CHOV, FIB:FIB, POLYL:POLYL, CHOCDF:CHOCDF, OA:OA,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIA:THIA, RIBF:RIBF, NIA:NIA, NE:NE, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			ALC:ALC, NACL_EQ:NACL_EQ,
			FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, FAPUN3:FAPUN3, FAPUN6:FAPUN6,
			FIBTG:FIBTG, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTDF:FIBTDF, FIBSDFS:FIBSDFS, FIBSDFP:FIBSDFP, FIBIDF:FIBIDF, STARES:STARES
		}, function( data ){
//			$( "#L3" ).html( data );
			$.post( kp + "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){
				$( "#L2" ).html( data );

				dl2 = true;
				dl3 = false;
				displayBW();
				displayVIDEO( food_name + ' saved' );
			});

		});
	} else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};

// Koyomi fix history
var koyomiFixHis = function( yyyy, mm, dd, tdiv ){
	var fix_his_code = document.getElementById( "fix_his_code" ).value;
	if( fix_his_code != '' ){
		$.post( kp + "koyomi-fix.cgi", { command:"history", yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, fix_his_code:fix_his_code }, function( data ){
			$( "#L3" ).html( data );
		});
	}
};

// Koyomi modify or copy panel fix
var koyomiFixR = function(){
	dl2 = true;
	dl3 = false;
	displayBW();
};

// Koyomi modify or copy panel fix
var modifyKoyomif = function( code, yyyy, mm, dd, tdiv, hh_mm, meal_time, order ){
	displayVIDEO( 'fix' );
	$.post( kp + "koyomi-fix.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time, order:order }, function( data ){
		$( "#L3" ).html( data );

		dl3 = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi import panel//////////////////////////////////////////////////////////////

// Koyomi insert panel
var addKoyomi = function( code ){
	pushBW();
	flashBW();
	$.post( kp + "koyomi-add.cgi", { command:"init", code:code }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
	$.post( kp + "koyomi.cgi", { command:"menu" }, function( data ){
		$( "#LINE" ).html( data );

		dline = true;
		displayBW();
	});

};

// Koyomi insert panel change
var changeKoyomiAdd = function( com, code, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var meal_time = document.getElementById( "meal_time" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	$.post( kp + "koyomi-add.cgi", { command:com, code:code, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, carry_on:carry_on, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

// Updating code into Koyomi
var saveKoyomiAdd = function( com, code, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh_mm = document.getElementById( "hh_mm" ).value;
	var meal_time = document.getElementById( "meal_time" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	var copy = 0;
	if( document.getElementById( "copy" )){
		if( document.getElementById( "copy" ).checked ){ copy = 1; }
	}
	$.post( kp + "koyomi-add.cgi", { command:com, code:code, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, carry_on:carry_on, origin:origin, copy:copy }, function( data ){
		$( "#LF" ).html( data );
	});
};

// Saving code into Koyomi direct
const saveKoyomiAdd_direct = function( code, yyyy, mm, dd, tdiv, origin ){
	const hh_mm = document.getElementById( "hh_mm" ).value;
	const meal_time = document.getElementById( "meal_time" ).value;
	const ev = document.getElementById( "ev" ).value;
	const eu = document.getElementById( "eu" ).value;
	let carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	$.post( kp + "koyomi-add.cgi", { command:"save", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, carry_on:carry_on, origin:origin }, function( data ){
			$( "#LF" ).html( data );
	});
};

// Modifying or copying code in Koyomi
const k2Koyomi_direct = function( com, code, yyyy, mm, dd, tdiv, origin ){
	const hh_mm = document.getElementById( "hh_mm" ).value;
	const meal_time = document.getElementById( "meal_time" ).value;
	const ev = document.getElementById( "ev" ).value;
	const eu = document.getElementById( "eu" ).value;
	let carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
 	let copy = 0;
 	if( document.getElementById( "copy" ).checked ){ copy = 1; }
	$.post( kp + "koyomi-add.cgi", { command:com, code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, carry_on:carry_on, origin:origin, copy:copy }, function( data ){
		$( "#LF" ).html( data );
	});
};


// Modifying or copying fix code in Koyomi
var modifysaveKoyomiFC = function( code, origin ){
	$.post( kp + "koyomi-add.cgi", { command:"move_fix", code:code, origin:origin, copy:1 }, function( data ){
		$( "#LF" ).html( data );

		pushBW();
		dlf = true;
		displayBW();
	});
};

// Return from Koyomi
var koyomiReturn = function(){
	pullBW();
	displayBW();
};

// Return from Koyomi to Koyomi edit
var koyomiReturn2KE = function( yyyy, mm, dd ){
	$.post( kp + "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){
		$( "#L2" ).html( data );

		pullBW();
		displayBW();
	});
};

// Koyomi modify or copy panel
var modifyKoyomi = function( com, code, yyyy, mm, dd, tdiv, hh_mm, meal_time, ev, eu, order ){
	$.post( kp + "koyomi-add.cgi", {command:com, code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time, ev:ev, eu:eu, order:order }, function( data ){
		$( "#LF" ).html( data );

		pushBW();
		dl2 = false;
		dlf = true;
		displayBW();
	});
};

// Koyomi insert panel change  for fix code
var modifychangeKoyomiFC = function( code, origin ){
	var hh = document.getElementById( "hh" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	$.post( kp + "koyomi-add.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, carry_on:carry_on, origin:origin }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};

// Set time to now
var nowKoyomi = function( id ){
	var today = new Date();
	var hh = today.getHours();
	var mm = today.getMinutes();
	if( hh < 10 ){ hh = '0' + hh; }
	if( mm < 10 ){ mm = '0' + mm; }
	document.getElementById( id ).value = hh + ':' + mm;
};

/////////////////////////////////////////////////////////////////////////////////
// Koyomi menu copy / move //////////////////////////////////////////////////////////////

var cmmKoyomi = function( cm_mode, yyyy, mm, dd, tdiv ){
	$.post( kp + "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv }, function( data ){
		$( "#LF" ).html( data );

		pushBW();
		flashBW();
		dlf = true;
		dline = true;
		displayBW();
	});
};

var cmmChangeKoyomi = function( cm_mode, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv_cmm" ).value;
	var hh_mm = document.getElementById( "hh_mm_cmm" ).value;
	var meal_time = document.getElementById( "meal_time_cmm" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	$.post( kp + "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, carry_on:carry_on, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

var cmmSaveKoyomi = function( cm_mode, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv_cmm" ).value;
	var hh_mm = document.getElementById( "hh_mm_cmm" ).value;
	var meal_time = document.getElementById( "meal_time_cmm" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	$.post( kp + "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, carry_on:carry_on, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

var cmmSaveKoyomi_direct = function( cm_mode, yyyy, mm, dd, tdiv, origin ){
	var hh_mm = document.getElementById( "hh_mm_cmm" ).value;
	var meal_time = document.getElementById( "meal_time_cmm" ).value;
	var carry_on = 0;
	if( document.getElementById( "carry_on" ).checked ){ carry_on = 1; }
	$.post( kp + "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, carry_on:carry_on, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi EX //////////////////////////////////////////////////////////////

// Koyomi EX init
var initKoyomiex = function(){
	$.post( kp + "koyomiex.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		dline = true;
		displayBW();
	});
};


// Koyomi EX change
var changeKoyomiex = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( kp + "koyomiex.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};


// Updating Koyomiex cell
var updateKoyomiex = function( kex_key, dd ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var cell = document.getElementById( kex_key + dd ).value;
	$.post( kp + "koyomiex.cgi", { command:"update", yyyy_mm:yyyy_mm, dd:dd, kex_key:kex_key, cell:cell }, function( data ){ $( "#L1" ).html( data );});
//	$.post( kp + "koyomiex.cgi", { command:"update", yyyy_mm:yyyy_mm, dd:dd, kex_key:kex_key, cell:cell }, function( data ){});
};


// Uploading table file
var importkoyomiex = function(){
	form_data = new FormData( $( '#table_form' )[0] );
	form_data.append( 'command', 'upload' );
	$.ajax( kp + "koyomiex-in.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){
				$( "#L2" ).html( data )

				dl1 = false;
				dl2 = true;
				dline = true;
				displayBW();
			;}
		}
	);
};


// Updating koyomiex with table file
//var writekoyomiex = function( file, size, msg ){
var writekoyomiex = function( file, size, msg ){
	if( document.getElementById( 'skip_line1' ).checked ){ var skip_line1 = 1; }else{ var skip_line1 = 0; }
	if( document.getElementById( 'overwrite' ).checked ){ var overwrite = 1; }else{ var overwrite = 0; }
	var date_flag = false;

	var items = [];
	for( i = 0; i < size; i++ ){
		if( document.getElementById( 'item' + i ) != null ){
			items[i] = document.getElementById( 'item' + i ).value;
			if( items[i] == 'date' ){
				date_flag = true;
			}
		}
	}
	var item_solid = items.join( ':' );

	if( date_flag ){
		$.post( kp + "koyomiex-in.cgi", { command:'update', file:file, skip_line1:skip_line1, overwrite:overwrite, item_solid:item_solid }, function( data ){
			$( "#L2" ).html( data );

//			initKoyomiex();
		});
	}else{
		displayVIDEO( msg );
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi calc //////////////////////////////////////////////////////////////

// Initiation
var initKoyomiCalc = function(){
	$.post( kp + "koyomi-calc.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dline = true;
		dl1 = true;
		displayBW();
	});
};

// Calculation
var calcKoyomiCalc = function(){
	var palette = document.getElementById( "palette" ).value;
	var fcz = document.getElementById( "fcz" ).value;
	var yyyymmdds = document.getElementById( "yyyymmdds" ).value;
	var yyyymmdde = document.getElementById( "yyyymmdde" ).value;
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( kp + "koyomi-calc.cgi", { command:"calc", palette:palette, fcz:fcz, yyyymmdds:yyyymmdds, yyyymmdde:yyyymmdde, ew_mode:ew_mode }, function( data ){ $( "#L1" ).html( data ); });
};

/////////////////////////////////////////////////////////////////////////////////
// Koyomi composition //////////////////////////////////////////////////////////////

// Koyomi composition
var initKoyomiCompo = function(){
	$.post( kp + "koyomi-compo.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dline= true;
		dl1 = true;
		displayBW();
	});
};

// Analysis composition
var calcKoyomiCompo = function(){
	var yyyymmdds = document.getElementById( "yyyymmdds" ).value;
	var yyyymmdde = document.getElementById( "yyyymmdde" ).value;
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( kp + "koyomi-compo.cgi", { command:"compo", yyyymmdds:yyyymmdds, yyyymmdde:yyyymmdde, ew_mode:ew_mode }, function( data ){ $( "#L1" ).html( data ); });
};

/////////////////////////////////////////////////////////////////////////////////
// Ginmi //////////////////////////////////////////////////////////////

// Ginmi init
const initGinmi = function(){
	flashBW();
	$.post( "ginmi.cgi", { mod:'menu' }, function( data ){
		$( "#LINE" ).html( data );

		flashBW();
		dline = true;
		dl1 = true;
		displayBW();
	});
	$.post( "ginmi.cgi", { mod:'' }, function( data ){
		$( "#L1" ).html( data );
	});
};

const ginmiForm = function( mod ){
	$.post( "ginmi.cgi", { mod:mod, command:'form' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dline = true;
		dl1 = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Physique //////////////////////////////////////////////////////////////

// Physique init
var initPhysique = function(){
	flashBW();
	$.post( "physique.cgi", { mod:'line' }, function( data ){
		$( "#LINE" ).html( data );

		dline = true;
		displayBW();
	});
	$.post( "physique.cgi", { mod:'' }, function( data ){
		$( "#L1" ).html( data );

		dl1 = true;
		displayBW();
	});
};

var PhysiqueForm = function( mod ){
	$.post( "physique.cgi", { mod:mod, step:'form' }, function( data ){
		$( "#L1" ).html( data );

		$.post( "physique.cgi", { mod:mod, step:'chart' }, function( data ){
			$( "#L2" ).html( data );

			$.post( "physique.cgi", { mod:mod, step:'notice', jsf:"1" }, function( data ){
				$( "#L3" ).html( data );
			
				dl2 = true;
				dl3 = true;
				displayBW();
			});
		});
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Mother and child //////////////////////////////////////////////////////////////

// Mother and child init
var initMomChai = function(){
	flashBW();
	$.post( "momchai.cgi", { mod:'line' }, function( data ){
		$( "#LINE" ).html( data );

		dline = true;
		displayBW();
	});
	$.post( "momchai.cgi", { mod:'' }, function( data ){
		$( "#L1" ).html( data );

		dl1 = true;
		displayBW();
	});
};

var MomChaiForm = function( mod ){
	$.post( "momchai.cgi", { mod:mod, step:'form' }, function( data ){ $( "#L1" ).html( data );});
	$.post( "momchai.cgi", { mod:mod, step:'chart' }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		displayBW();
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Elderly //////////////////////////////////////////////////////////////

// Elderly init
var initElderly = function(){

};


/////////////////////////////////////////////////////////////////////////////////
// Pathology //////////////////////////////////////////////////////////////

// Pathology init
var initPathology = function(){

};


/////////////////////////////////////////////////////////////////////////////////
// Food rank //////////////////////////////////////////////////////////////

// Dosplaying recipe by scatter plott
const foodRank = function(){
	$.post( "food-rank.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Dosplaying recipe by scatter plott
const foodRankList = function(){
	const main_item = document.getElementById( "main_item" ).value;
	const comp_item = document.getElementById( "comp_item" ).value;
	const rank_order = document.getElementById( "rank_order" ).value;
	const rank_display = document.getElementById( "rank_display" ).value;
	const fg = document.getElementById( "fg" ).value;

	let ex_inf = 0;
	let ex_zero = 0;
	if( document.getElementById( "ex_inf" ).checked ){ ex_inf = 1; }
	if( document.getElementById( "ex_zero" ).checked ){ ex_zero = 1; }

	$.post( "food-rank.cgi", { command:'list', fg:fg, main_item:main_item, comp_item:comp_item, rank_order:rank_order, rank_display:rank_display, ex_inf:ex_inf, ex_zero:ex_zero }, function( data ){
		$( "#L1" ).html( data );
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Note //////////////////////////////////////////////////////////////

// Note book
const initNote = function(){
	$.post( "note.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Note book
const writeNote = function(){
	const note = document.getElementById( "note" ).value;
	if( note != '' ){
		$.post( "note.cgi", { command:'write', note:note }, function( data ){ $( "#L1" ).html( data );});
	}
};

// Note book
const deleteNote = function( code ){
	if( document.getElementById( code ).checked ){
		$.post( "note.cgi", { command:'delete', code:code, base:'note', secure:'1' }, function( data ){
			$( "#L1" ).html( data );}
		);
		displayVIDEO( 'Deleted' );
	}else{
		displayVIDEO( 'Check!(>_<)' );
	}
};


/////////////////////////////////////////////////////////////////////////////////
// FCZ edit //////////////////////////////////////////////////////////////

// FCZ list init
var initFCZlist = function(){
	$.post( "fcz-list.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// FCZ list change
var baseFCZlist = function( page ){
	var base = document.getElementById( "base_select" ).value;
	$.post( "fcz-list.cgi", { command:'init', base:base, page:page }, function( data ){ $( "#L1" ).html( data ); });
};

// FCZ list delete
var deleteFCZlist = function( fcz_code, page ){
	var base = document.getElementById( "base_select" ).value;
	if( document.getElementById( fcz_code ).checked ){
		$.post( "fcz-list.cgi", { command:'delete', base:base, page:page, fcz_code:fcz_code }, function( data ){ $( "#L1" ).html( data ); });
	}else{
		displayVIDEO( 'Check!(>_<)' );
	}
};

// FCZ editor
var initFCZedit = function( fcz_code ){
	var base = document.getElementById( "base_select" ).value;
	$.post( "fcz-edit.cgi", { command:'init', base:base, fcz_code:fcz_code }, function( data ){
		$( "#L2" ).html( data );

		dl1 = false;
		dl2 = true;
		displayBW();
	});
};


// FCZ editor save
var saveFCZedit = function( fcz_code ){
	var base = document.getElementById( "base" ).value;
	var fcz_name = document.getElementById( "fcz_name" ).value;
	var origin = document.getElementById( "origin" ).value;

	var ENERC = document.getElementById( "zENERC" ).value;
	var ENERC_KCAL = document.getElementById( "zENERC_KCAL" ).value;
	var WATER = document.getElementById( "zWATER" ).value;

	var PROTCAA = document.getElementById( "zPROTCAA" ).value;
	var PROT = document.getElementById( "zPROT" ).value;
	var PROTV = document.getElementById( "zPROTV" ).value;
	var FATNLEA = document.getElementById( "zFATNLEA" ).value;
	var CHOLE = document.getElementById( "zCHOLE" ).value;
	var FAT = document.getElementById( "zFAT" ).value;
	var FATV = document.getElementById( "zFATV" ).value;
	var CHOAVLM = document.getElementById( "zCHOAVLM" ).value;
	var CHOAVL = document.getElementById( "zCHOAVL" ).value;
	var CHOAVLDF = document.getElementById( "zCHOAVLDF" ).value;
	var CHOV = document.getElementById( "zCHOV" ).value;
	var FIB = document.getElementById( "zFIB" ).value;
	var POLYL = document.getElementById( "zPOLYL" ).value;
	var CHOCDF = document.getElementById( "zCHOCDF" ).value;
	var OA = document.getElementById( "zOA" ).value;

	var ASH = document.getElementById( "zASH" ).value;
	var NA = document.getElementById( "zNA" ).value;
	var K = document.getElementById( "zK" ).value;
	var CA = document.getElementById( "zCA" ).value;
	var MG = document.getElementById( "zMG" ).value;
	var P = document.getElementById( "zP" ).value;
	var FE = document.getElementById( "zFE" ).value;
	var ZN = document.getElementById( "zZN" ).value;
	var CU = document.getElementById( "zCU" ).value;
	var MN = document.getElementById( "zMN" ).value;
	var ID = document.getElementById( "zID" ).value;
	var SE = document.getElementById( "zSE" ).value;
	var CR = document.getElementById( "zCR" ).value;
	var MO = document.getElementById( "zMO" ).value;

	var RETOL = document.getElementById( "zRETOL" ).value;
	var CARTA = document.getElementById( "zCARTA" ).value;
	var CARTB = document.getElementById( "zCARTB" ).value;
	var CRYPXB = document.getElementById( "zCRYPXB" ).value;
	var CARTBEQ = document.getElementById( "zCARTBEQ" ).value;
	var VITA_RAE = document.getElementById( "zVITA_RAE" ).value;
	var VITD = document.getElementById( "zVITD" ).value;
	var TOCPHA = document.getElementById( "zTOCPHA" ).value;
	var TOCPHB = document.getElementById( "zTOCPHB" ).value;
	var TOCPHG = document.getElementById( "zTOCPHG" ).value;
	var TOCPHD = document.getElementById( "zTOCPHD" ).value;
	var VITK = document.getElementById( "zVITK" ).value;

	var THIA = document.getElementById( "zTHIA" ).value;
	var RIBF = document.getElementById( "zRIBF" ).value;
	var NIA = document.getElementById( "zNIA" ).value;
	var NE = document.getElementById( "zNE" ).value;
	var VITB6A = document.getElementById( "zVITB6A" ).value;
	var VITB12 = document.getElementById( "zVITB12" ).value;
	var FOL = document.getElementById( "zFOL" ).value;
	var PANTAC = document.getElementById( "zPANTAC" ).value;
	var BIOT = document.getElementById( "zBIOT" ).value;
	var VITC = document.getElementById( "zVITC" ).value;

	var ALC = document.getElementById( "zALC" ).value;
	var NACL_EQ = document.getElementById( "zNACL_EQ" ).value;

	var FASAT = document.getElementById( "zFASAT" ).value;
	var FAMS = document.getElementById( "zFAMS" ).value;
	var FAPU = document.getElementById( "zFAPU" ).value;
	var FAPUN3 = document.getElementById( "zFAPUN3" ).value;
	var FAPUN6 = document.getElementById( "zFAPUN6" ).value;

	var FIBTG = document.getElementById( "zFIBTG" ).value;
	var FIBSOL = document.getElementById( "zFIBSOL" ).value;
	var FIBINS = document.getElementById( "zFIBINS" ).value;
	var FIBTDF = document.getElementById( "zFIBTDF" ).value;
	var FIBSDFS = document.getElementById( "zFIBSDFS" ).value;
	var FIBSDFP = document.getElementById( "zFIBSDFP" ).value;
	var FIBIDF = document.getElementById( "zFIBIDF" ).value;
	var STARES = document.getElementById( "zSTARES" ).value;

	$.post( "fcz-edit.cgi", {
		command:'save', fcz_code:fcz_code, base:base, fcz_name:fcz_name, origin:origin, food_code:null, food_name:null, food_weight:100,
		ENERC:ENERC, ENERC_KCAL:ENERC_KCAL, WATER:WATER,
		PROTCAA:PROTCAA, PROT:PROT, PROTV:PROTV, FATNLEA:FATNLEA, CHOLE:CHOLE, FAT:FAT, FATV:FATV, CHOAVLM:CHOAVLM, CHOAVL:CHOAVL, CHOAVLDF:CHOAVLDF, CHOV:CHOV, FIB:FIB, POLYL:POLYL, CHOCDF:CHOCDF, OA:OA,
		ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
		RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
		THIA:THIA, RIBF:RIBF, NIA:NIA, NE:NE, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
		ALC:ALC, NACL_EQ:NACL_EQ,
		FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, FAPUN3:FAPUN3, FAPUN6:FAPUN6,
		FIBTG:FIBTG, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTDF:FIBTDF, FIBSDFS:FIBSDFS, FIBSDFP:FIBSDFP, FIBIDF:FIBIDF, STARES:STARES
	}, function( data ){
//			$( "#L2" ).html( data );
		$.post( "fcz-list.cgi", { command:'init', base:base }, function( data ){
			$( "#L1" ).html( data );

			dl1 = true;
			dl2 = false;
			displayBW();
			displayVIDEO( 'saved' );
		});

	});
};

// FCZ edit return
var fczlReturn = function(){
	dl1 = true;
	dl2 = false;
	displayBW();
};

/////////////////////////////////////////////////////////////////////////////////
// Ref instake //////////////////////////////////////////////////////////////

// Ref instake init
var initRefIntake = function(){
	$.post( "ref-intake.cgi", { command:'menu' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Ref instake init
var viewRefIntake = function(){
	var rits_item = document.getElementById( "rits_item" ).value;
	$.post( "ref-intake.cgi", { command:'view_item', rits_item:rits_item }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		displayBW();
	});
};


// Ref instake personal
var viewRefIntakeP = function(){
	var ritp_age = document.getElementById( "ritp_age" ).value;
	var ritp_age_mode = document.getElementById( "ritp_age_mode" ).value;
	if( document.getElementById( "sex_m" ).checked ){ var sex = 0; }else{ var sex = 1; }
	if( document.getElementById( "ff_m" ).checked ){ var ff_m = 1; }else{ var ff_m = 0; }
	if( document.getElementById( "ff_non" ).checked ){ var ff_c = 0; }
	if( document.getElementById( "ff_p1" ).checked ){ var ff_c = 1; }
	if( document.getElementById( "ff_p2" ).checked ){ var ff_c = 2; }
	if( document.getElementById( "ff_p3" ).checked ){ var ff_c = 3; }
	if( document.getElementById( "ff_l" ).checked ){ var ff_c = 4; }

	$.post( "ref-intake.cgi", { command:'personal', ritp_age:ritp_age, ritp_age_mode:ritp_age_mode, sex:sex, ff_m:ff_m, ff_c:ff_c }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		displayBW();
	});
};

// Ref instake personal
var saveRefIntake = function(){
	var ritp_age = document.getElementById( "ritp_age" ).value;
	var ritp_age_mode = document.getElementById( "ritp_age_mode" ).value;
	var fcz_name = document.getElementById( "fcz_name" ).value;
	if( document.getElementById( "sex_m" ).checked ){ var sex = 0; }else{ var sex = 1; }
	if( document.getElementById( "ff_m" ).checked ){ var ff_m = 1; }else{ var ff_m = 0; }
	if( document.getElementById( "ff_non" ).checked ){ var ff_c = 0; }
	if( document.getElementById( "ff_p1" ).checked ){ var ff_c = 1; }
	if( document.getElementById( "ff_p2" ).checked ){ var ff_c = 2; }
	if( document.getElementById( "ff_p3" ).checked ){ var ff_c = 3; }
	if( document.getElementById( "ff_l" ).checked ){ var ff_c = 4; }

	if( fcz_name != '' ){
		$.post( "ref-intake.cgi", { command:'save', ritp_age:ritp_age, ritp_age_mode:ritp_age_mode, sex:sex, ff_m:ff_m, ff_c:ff_c, fcz_name:fcz_name }, function( data ){
//			$( "#L4" ).html( data );

//			dl4 = true;
//			displayBW();
			displayVIDEO( 'Saved FCZ' );
		});
	}else{
		displayVIDEO( 'FCZ name!(>_<)' );
	}
};
