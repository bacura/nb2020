//guild.js ver 0.05b 20220119

/////////////////////////////////////////////////////////////////////////////////
// Koyomi //////////////////////////////////////////////////////////////

// Koyomi
var initKoyomi = function(){
	flashBW();
	$.post( "koyomi.cgi", { command:"menu" }, function( data ){
		$( "#LINE" ).html( data );
		dl1 = true;
		displayBW();
	});
	$.post( "koyomi.cgi", { command:"init" }, function( data ){
		$( "#L1" ).html( data );
		dline = true;
		displayBW();
	});
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
	$.post( "koyomi-edit.cgi", { command:com, yyyy_mm:yyyy_mm, dd:dd }, function( data ){
		$( "#L2" ).html( data );
		flashBW();
		dl2 = true;
		dline = true;
		displayBW();
	});
};

// Koyomi delete
var deleteKoyomi = function( yyyy, mm, dd, tdiv, code, order ){
	$.post( "koyomi-edit.cgi", { command:'delete', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, code:code, order:order }, function( data ){ $( "#L2" ).html( data );});
};

// Koyomi memo
var memoKoyomi = function( yyyy, mm, dd ){
	var memo = document.getElementById( "memo" ).value;
	$.post( "koyomi-edit.cgi", { command:'memo', yyyy:yyyy, mm:mm, dd:dd, memo:memo }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'memo saved');
	});
};

// Koyomi Save Something
var koyomiSaveSome = function( yyyy, mm, dd, tdiv, id ){
	var some = document.getElementById( id ).value;
	$.post( "koyomi-edit.cgi", { command:'some', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:99, some:some }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Something saved' );
	});
};

// Koyomi edit return
var editKoyomiR = function( yyyy, mm ){
	$.post( "koyomi.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		dl2 = false;
		displayBW();
	});
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
	$.post( "photo.cgi", { command:'delete', code:code, mcode:mcode, base:'koyomi' }, function( data ){
		editKoyomi( 'init', dd );
	});
//	setTimeout( editKoyomi( 'init', dd ), 2000);
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi calc //////////////////////////////////////////////////////////////

// Koyomi calc
var calcKoyomi = function( yyyy, mm, dd, palette ){
	if( palette ){ var palette = document.getElementById( "palette" ).value; }

	$.post( "koyomi-calc.cgi", { command:"init", yyyy:yyyy, mm:mm, dd:dd, palette:palette }, function( data ){
		$( "#L2" ).html( data );

		dl1 = false;
		dl2 = true;
		displayBW();
	});
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
	$.post( "koyomi-fix.cgi", { command:com, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv }, function( data ){
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
	var hh_mm = document.getElementById( "hh_mm_fix" ).value;
	var meal_time = document.getElementById( "meal_time_fix" ).value;
	var food_number = document.getElementById( "food_number" ).value;

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
		var FATNLEA = document.getElementById( "kfFATNLEA" ).value;
		var CHOLE = document.getElementById( "kfCHOLE" ).value;
		var FAT = document.getElementById( "kfFAT" ).value;
		var CHOAVLM = document.getElementById( "kfCHOAVLM" ).value;
		var CHOAVL = document.getElementById( "kfCHOAVL" ).value;
		var CHOAVLMF = document.getElementById( "kfCHOAVLMF" ).value;
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

		$.post( "koyomi-fix.cgi", {
			command:'save', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time,meal_time,
			food_name:food_name, food_weight:food_weight, food_number:food_number, modifyf:modifyf, order:order,
			ENERC:ENERC, ENERC_KCAL:ENERC_KCAL, WATER:WATER,
			PROTCAA:PROTCAA, PROT:PROT, FATNLEA:FATNLEA, CHOLE:CHOLE, FAT:FAT, CHOAVLM:CHOAVLM, CHOAVL:CHOAVL, CHOAVLMF:CHOAVLMF, FIB:FIB, POLYL:POLYL, CHOCDF:CHOCDF, OA:OA,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIA:THIA, RIBF:RIBF, NIA:NIA, NE:NE, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			ALC:ALC, NACL_EQ:NACL_EQ
		}, function( data ){
			$( "#L3" ).html( data );
			$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){
				$( "#L2" ).html( data );

				dl2 = true;
				dl3 = false;
				displayBW();
				displayVIDEO( food_name + ' saved' );
			});

		});


//		var fx = function(){
//			$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#L2" ).html( data );});
//		};
//		setTimeout( fx , 1000 );
	} else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};


// Koyomi modify or copy panel fix
var koyomiFixR = function(){
	dl2 = true;
	dl3 = false;
	displayBW();
};

// Koyomi modify or copy panel fix
var modifyKoyomif = function( code, yyyy, mm, dd, tdiv, hh, order ){
	$.post( "koyomi-fix.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, order:order }, function( data ){
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
	$.post( "koyomi-add.cgi", { command:"init", code:code }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
	$.post( "koyomi.cgi", { command:"menu" }, function( data ){
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
	$.post( "koyomi-add.cgi", { command:com, code:code, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

// Updating code into Koyomi
var saveKoyomiAdd = function( com, code, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh_mm = document.getElementById( "hh_mm" ).value;
	var meal_time = document.getElementById( "meal_time" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var copy = 0;
	if( document.getElementById( "copy" )){
		if( document.getElementById( "copy" ).checked ){ copy = 1; }
	}
	$.post( "koyomi-add.cgi", { command:com, code:code, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, origin:origin, copy:copy }, function( data ){
		$( "#LF" ).html( data );

		dlf = false;
		displayBW();

		if( com == 'move' ){
			$.post( "koyomi-edit.cgi", { command:'init', yyyy_mm_dd:yyyy_mm_dd }, function( data ){
				$( "#L2" ).html( data );

				dl2 = true;
				displayBW();
			});
		}
	});
//	if( com == 'move' ){
//		dl2 = true;
//		dlf = false;
//		displayBW();
//		var fx = function(){ $.post( "koyomi-edit.cgi", { command:'init', yyyy_mm_dd:yyyy_mm_dd }, function( data ){ $( "#L2" ).html( data );}); }
//		setTimeout( fx() , 1000 );
//	}
};

// Saving code into Koyomi direct
var saveKoyomiAdd_direct = function( code, yyyy, mm, dd, tdiv, origin ){
	var hh_mm = document.getElementById( "hh_mm" ).value;
	var meal_time = document.getElementById( "meal_time" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	$.post( "koyomi-add.cgi", { command:"save", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

// Modifying or copying code in Koyomi
var modifysaveKoyomi_direct = function( code, yyyy, mm, dd, tdiv, origin ){
	var hh_mm = document.getElementById( "hh_mm" ).value;
	var meal_time = document.getElementById( "meal_time" ).value;
	var copy = 0;
	if( document.getElementById( "copy" ).checked ){ copy = 1; }
	$.post( "koyomi-add.cgi", { command:"move", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, origin:origin, copy:copy }, function( data ){
		$( "#LF" ).html( data );

		dlf = false;
		displayBW();

		$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){
			$( "#L2" ).html( data );

			dl2 = true;
			displayBW();
		});
	});


//	var fx = function(){ $.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#L2" ).html( data );}); }
//	setTimeout( fx() , 1000 );
};

// Modifying or copying fix code in Koyomi
var modifysaveKoyomiFC = function( code, origin ){
	$.post( "koyomi-add.cgi", { command:"move_fix", code:code, origin:origin, copy:1 }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});


};

// Return from Koyomi
var koyomiReturn = function(){
	pullHW();
	displayBW();
};

// Return from Koyomi to Koyomi edit
var koyomiReturn2KE = function( yyyy, mm, dd ){
	$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){
		$( "#L2" ).html( data );

		pullHW();
		displayBW();
	});
};

// Koyomi modify or copy panel
var modifyKoyomi = function( code, yyyy, mm, dd, tdiv, hh, ev, eu, order ){
	$.post( "koyomi-add.cgi", {command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, order:order }, function( data ){
		$( "#LF" ).html( data );

		dl2 = false;
		dlf = true;
		displayBW();
	});
};

// Koyomi insert panel change  for fix code
var modifychangeKoyomiFC = function( code, origin ){
	var hh = document.getElementById( "hh" ).value;
	$.post( "koyomi-add.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){
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
	$.post( "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv }, function( data ){
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
	$.post( "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

var cmmSaveKoyomi = function( cm_mode, origin ){
	var yyyy_mm_dd = document.getElementById( "yyyy_mm_dd" ).value;
	var tdiv = document.getElementById( "tdiv_cmm" ).value;
	var hh_mm = document.getElementById( "hh_mm_cmm" ).value;
	var meal_time = document.getElementById( "meal_time_cmm" ).value;

	$.post( "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy_mm_dd:yyyy_mm_dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};

var cmmSaveKoyomi_direct = function( cm_mode, yyyy, mm, dd, tdiv, origin ){
	var hh_mm = document.getElementById( "hh_mm_cmm" ).value;
	var meal_time = document.getElementById( "meal_time_cmm" ).value;
	$.post( "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time:meal_time, origin:origin }, function( data ){ $( "#LF" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi EX //////////////////////////////////////////////////////////////

// Koyomi EX init
var initKoyomiex = function(){
	$.post( "koyomiex.cgi", { command:"init" }, function( data ){
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
	$.post( "koyomiex.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};


// Updating Koyomiex cell
var updateKoyomiex = function( dd, item_no, cell_id ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	var cell = document.getElementById( cell_id ).value;
//	$.post( "koyomiex.cgi", { command:"update", yyyy_mm:yyyy_mm, dd:dd, item_no:item_no, cell:cell }, function( data ){ $( "#L1" ).html( data );});
	$.post( "koyomiex.cgi", { command:"update", yyyy_mm:yyyy_mm, dd:dd, item_no:item_no, cell:cell }, function( data ){});
};


// Uploading table file
var importkoyomiex = function(){
	form_data = new FormData( $( '#table_form' )[0] );
	form_data.append( 'command', 'upload' );
	$.ajax( "koyomiex-in.cgi",
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
var writekoyomiex = function( file, size, msg ){
	if( document.getElementById( 'skip_line1' ).checked ){ skip_line1 = 1; }else{ var skip_line1 = 0; }
	if( document.getElementById( 'overwrite' ).checked ){ overwrite = 1; }else{ var soverwrite = 0; }
	var date_flag= false;

	var items = [];
	for( i = 0; i < size; i++ ){
		if( document.getElementById( 'item' + i ) != null ){ items[i] = document.getElementById( 'item' + i ).value; }
		if( items[i] == '99' ){ date_flag = true; }
	}
	var item_solid = items.join( ':' );

	if( date_flag ){
		$.post( "koyomiex-in.cgi", { command:'update', file:file, skip_line1:skip_line1, overwrite:overwrite, item_solid:item_solid }, function( data ){
			$( "#L2" ).html( data );

			initKoyomiex();
		});
	}else{
		displayVIDEO( msg );
	}

//	setTimeout( initKoyomiex(), 1000 );
};


/////////////////////////////////////////////////////////////////////////////////
// Ginmi //////////////////////////////////////////////////////////////

// Ginmi init
var initGinmi = function(){
	flashBW();
	$.post( "ginmi.cgi", { mod:'line' }, function( data ){
		$( "#LINE" ).html( data );

		dline = true;
		displayBW();
	});
	$.post( "ginmi.cgi", { mod:'' }, function( data ){
		$( "#L1" ).html( data );

		dl1 = true;
		displayBW();
	});
};

var ginmiForm = function( mod ){
	$.post( "ginmi.cgi", { mod:mod, command:'form' }, function( data ){
		$( "#L1" ).html( data );

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
	$.post( "physique.cgi", { mod:mod, step:'form' }, function( data ){ $( "#L1" ).html( data ); });
	$.post( "physique.cgi", { mod:mod, step:'chart' }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		displayBW();
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


