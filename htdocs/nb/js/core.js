// Nutorition Browser 2020 core.js 0.6.6 (2024/06/16)
///////////////////////////////////////////////////////////////////////////////////
// Global ////////////////////////////////////////////////////////////////////
dl1 = false;
dl2 = false;
dl3 = false;
dl4 = false;
dl5 = false;
dlf = false;
dline = false;

hl1 = false;
hl2 = false;
hl3 = false;
hl4 = false;
hl5 = false;
hlf = false;
hline = false;

world = null
bwl1 = null;
bwl2 = null;
bwl3 = null;
bwl4 = null;
bwl5 = null;
bwlf = null;
line = null;
video = null;

help = null;
help_tp = '1154';

menu_status = 0;
general_ = '';


/////////////////////////////////////////////////////////////////////////////////
// Paging /////////////////////////////////////////////////////////////////////////

// initialization
window.onload = function(){
	if( !!document.getElementById( "L1" )){
		world = document.getElementById( "WORLD" );
		bwl1 = document.getElementById( "L1" );
		bwl2 = document.getElementById( "L2" );
		bwl3 = document.getElementById( "L3" );
		bwl4 = document.getElementById( "L4" );
		bwl5 = document.getElementById( "L5" );
		bwlf = document.getElementById( "LF" );
		line = document.getElementById( "LINE" );
		video = document.getElementById( "VIDEO" );
		help = document.getElementById( "HELP" );

		toHelp();
	}
};


// Closing browse windows
// This feature will be discontinued in the future.
closeBroseWindows = function( num ){
	switch( Number( num )){
	case 0: document.getElementById( "L1" ).style.display = 'none';
	case 1: document.getElementById( "L2" ).style.display = 'none';
	case 2: document.getElementById( "L3" ).style.display = 'none';
	case 3: document.getElementById( "L4" ).style.display = 'none';
	case 4: document.getElementById( "L5" ).style.display = 'none';
	case 5: document.getElementById( "LF" ).style.display = 'none';
 	}
}


// Reopening browse windows
displayBW = function(){
	if( dl1 ){ bwl1.style.display = 'block'; }else{ bwl1.style.display = 'none'; }
	if( dl2 ){ bwl2.style.display = 'block'; }else{ bwl2.style.display = 'none'; }
	if( dl3 ){ bwl3.style.display = 'block'; }else{ bwl3.style.display = 'none'; }
	if( dl4 ){ bwl4.style.display = 'block'; }else{ bwl4.style.display = 'none'; }
	if( dl5 ){ bwl5.style.display = 'block'; }else{ bwl5.style.display = 'none'; }
	if( dlf ){ bwlf.style.display = 'block'; }else{ bwlf.style.display = 'none'; }
	if( dline ){ line.style.display = 'block'; }else{ line.style.display = 'none'; }
}


// Resetting level status
flashBW = function(){
	dl1 = false;
	dl2 = false;
	dl3 = false;
	dl4 = false;
	dl5 = false;
	dlf = false;
	dline = false;
}


// Pushing level status to hide
pushBW = function(){
	hl1 = dl1;
	hl2 = dl2;
	hl3 = dl3;
	hl4 = dl4;
	hl5 = dl5;
	hlf = dlf;
	hline = dline;
}


// Pulling level status from hide
pullBW = function(){
	dl1 = hl1;
	dl2 = hl2;
	dl3 = hl3;
	dl4 = hl4;
	dl5 = hl5;
	dlf = hlf;
	dline = hline;
}


// Opning menu LINE
// This feature will be discontinued in the future.
displayLINE = function( msg ){
	if( msg == 'on' ){
		line.style.display = 'block';
	}else if( msg == 'off' ){
		line.style.display = 'none';
	}else{
		line.style.display = 'block';
		line.innerHTML = msg;
	}
}


// Displaying message on VIDEO
displayVIDEO = function( msg ){
	video.innerHTML = msg;
	video.style.display = 'block';
	video.style.color = 'lime';
	var fx = function(){
		video.innerHTML = "";
		video.style.display = 'none';
	};
	setTimeout( fx, 2000 );
}


// Displaying message on VIDEO rec mode
displayREC = function(){
	video.innerHTML = "●";
	video.style.display = 'block';
	video.style.color = 'orangered';
	var fx = function(){
		video.innerHTML = "";
		video.style.display = 'none';
	};
	setTimeout( fx, 1000 );
}


// Exchanging menu sets
changeMenu = function( user_status ){
	switch( menu_status ){
		case 0:
			document.getElementById( "guild_menu" ).style.display = 'inline';
			displayVIDEO( 'Guild menu' );
			if( user_status >= 5 && user_status != 6 ){ menu_status = 1; }else{ menu_status = 3; }
			break;
		case 1:
			document.getElementById( "guild_menu" ).style.display = 'none';
			document.getElementById( "gs_menu" ).style.display = 'inline';
			displayVIDEO( 'Guild Shun menu' );
			if( user_status >= 8 ){ menu_status = 2; }else{ menu_status = 3; }
			break;
		case 2:
			document.getElementById( "gs_menu" ).style.display = 'none';
			document.getElementById( "gm_menu" ).style.display = 'inline';
			displayVIDEO( 'GM menu' );
			menu_status = 3;
			break;
		case 3:
			document.getElementById( "guild_menu" ).style.display = 'none';
			document.getElementById( "gs_menu" ).style.display = 'none';
			document.getElementById( "gm_menu" ).style.display = 'none';
			displayVIDEO( 'Standard menu' );
			menu_status = 0;
			break;
	}
}


// changing help to
toHelp = function( page ){
	if( page==null ){
		help.innerHTML = "<a href='https://bacura.jp/?page_id=" + help_tp + "' target='manual'><img src='bootstrap-dist/icons/question-circle-gray.svg' style='height:3em; width:2em;'></a>";
	}else{
		help.innerHTML = "<a href='https://bacura.jp/?page_id=" + page + "'' target='manual'><img src='bootstrap-dist/icons/question-circle-ndsk.svg' style='height:3em; width:2em;'></a>";
	}
}

//
modalPhoto = function( code ){
	$.post( "photo.cgi", { command:'modal_body', code:code }, function( data ){
		$( "#modal_body" ).html( data );
		$.post( "photo.cgi", { command:'modal_label', code:code }, function( data ){
			$( "#modal_label" ).html( data );
			$( '#modal' ).modal( 'show' );
		});
	});
}

/////////////////////////////////////////////////////////////////////////////////
// Account /////////////////////////////////////////////////////////////////////////
// Changing Account
chageAccountM = function(){
	var login_mv = document.getElementById( "login_mv" ).value;
	location.href = "login.cgi?mode=family" + "&login_mv=" + login_mv;
}


/////////////////////////////////////////////////////////////////////////////////
// Browsing nutritional Information /////////////////////////////////////////////////////////////////////

// Display foods on BWL1
var summonL1 = function( num ){
	$.get( "square.cgi", { channel:"fctb", category:num }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};


// Display foods on BWL2
var summonL2 = function( key ){
	$.get( "square.cgi", { channel:"fctb_l2", food_key:key }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};


// Display foods on BWL3
var summonL3 = function( key, direct ){
	if( direct > 0 ){ closeBroseWindows( direct ); }
	$.get( "square.cgi", { channel:"fctb_l3", food_key:key }, function( data ){
		$( "#L3" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		dl3 = true;
		displayBW();
	});
};


// Display foods on BWL4
var summonL4 = function( key, direct ){
	if( direct > 0 ){ closeBroseWindows( direct ); }
	$.get( "square.cgi", { channel:"fctb_l4", food_key:key }, function( data ){
		$( "#L4" ).html( data );

		dl4 = true;
		dl5 = false;
		dlf = false;
		displayBW();
	});
};


//////////////////////////////////////////////////////////////////////////////////
// Browsing nutritional Information subset ///////////////////////////////////////////////////////////////////////

// Display foods on BWL5
const viewDetailSub = function( com, key, direct ){
	if( direct > 0 ){ closeBroseWindows( direct ); }
	$.post( "detail-sub.cgi", { command:com, food_key:key }, function( data ){ $( "#L5" ).html( data );});
	dl5 = true;
	dlf = false;
	displayBW();
};


// Changing weight of food
const changeDSWeight = function( com, key, fn ){
	const fraction_mode = document.getElementById( "fraction" ).value;
	const weight = document.getElementById( "weight" ).value;
	$.post( "detail-sub.cgi", { command:com, food_key:key, frct_mode:fraction_mode, food_weight:weight, food_no:fn }, function( data ){
		$( "#L5" ).html( data );
		displayVIDEO( '(>_<)' );

	});
};


//////////////////////////////////////////////////////////////////////////////////
// Browsing nutritional Information (ditail) ///////////////////////////////////////////////////////////////////////

// Display ditail information on LF
var detailView = function( fn ){
	var fraction_mode = document.getElementById( "fraction" ).value;
	var food_weight = document.getElementById( "weight" ).value;
	$.post( "detail.cgi", { food_no:fn, frct_mode:fraction_mode, food_weight:food_weight, selectu:'g' }, function( data ){
		$( "#LF" ).html( data );

		pushBW();
		dl5 = false;
		dlf = true;
		displayBW();
	});
};

// Display ditail information on LF (history)
var detailView_his = function( fn ){
	$.post( "detail.cgi", { food_no:fn, frct_mode:1, food_weight:100, selectu:'g' }, function( data ){
		$( "#LF" ).html( data );

		pushBW();
		dline = false;
		dl1 = false;
		dlf = true;
		displayBW();
	});
};

// Changing weight of food (ditail)
var detailWeight = function( fn ){
	var fraction_mode = document.getElementById( "detail_fraction" ).value;
	var food_weight = document.getElementById( "detail_volume" ).value;
	var selectu = document.getElementById( "detail_unit" ).value;
	$.post( "detail.cgi", { food_no:fn, frct_mode:fraction_mode, food_weight:food_weight, selectu:selectu }, function( data ){ $( "#LF" ).html( data );});
};

// 詳細画面のページボタンを押したらL5閲覧ウインドウの内容を書き換える。
var detailReturn = function(){
	pullBW();
	displayBW();
};


/////////////////////////////////////////////////////////////////////////////////
// Referencing /////////////////////////////////////////////////////////////////////////

// Disply results
const search = function(){
	const words = document.getElementById( "words" ).value;
	const qcate = document.getElementById( "qcate" ).value;
	if( words != '' ){
		flashBW();
		switch( qcate ){
		case '0':
			$.post( "search-food.cgi", { words:words }, function( data ){
				$( "#L1" ).html( data );
		 		dl1 = true;
		 		displayBW();
			});
			break;
		case '1':
			$.post( "recipel.cgi", { command:'refer', words:words }, function( data ){
				$( "#L1" ).html( data );
		 		dl1 = true;
		 		displayBW();
			});
			break;
		case '2':
			$.post( "memory.cgi", { command:'refer', words:words, depth:1 }, function( data ){
				$( "#L1" ).html( data );
		 		dl1 = true;
		 		pushBW();
		 		displayBW();
			});
			break;
 		}
	}
};

// Direct recipe search
var searchDR = function( words ){
	$.post( "recipel.cgi", { command:'refer', words:words }, function( data ){
		$( "#L1" ).html( data );

		words = document.getElementById( "words" ).value = words;
		qcate = document.getElementById( "qcate" ).value = 1;

	 	flashBW();
	 	dl1 = true;
	 	displayBW();
	});
};

// Sending alias request
var aliasRequest = function( food_no ){
	document.getElementById( "LF" ).style.display = 'block';
	var alias = document.getElementById( "alias" ).value;
	if( alias != '' && alias != general_ ){
		$.post( "alias-req.cgi", { food_no:food_no, alias:alias }, function( data ){
			displayVIDEO( 'Request sent' );
		});
	}else if( alias == general_ ){
		displayVIDEO( 'Request sent' );
	}else{
		displayVIDEO( 'Alias! (>_<)' );
	}
	general_ = alias;
};


// Copy to words
cp2words = function( words, qcate ){
	document.getElementById( "words" ).value = words;
	if( qcate != '' ){ document.getElementById( "qcate" ).value = qcate; }
	$( '#modal_tip' ).modal( 'hide' );
	displayVIDEO( 'Picked' );
};


/////////////////////////////////////////////////////////////////////////////////
// history /////////////////////////////////////////////////////////////////////////

const historyInit = function(){
	flashBW();
	$.post( "history.cgi", { command:'menu' }, function( data ){
		$( "#LINE" ).html( data );

		$.post( "history.cgi", { command:'init', sub_fg:'init' }, function( data ){
			$( "#L1" ).html( data );

			dline = true;
			dl1 = true;
			displayBW();
			pushBW();
		});
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Puseudo food //////////////////////////////////////////////////////////////////////

// カテゴリーボタンを押したときに非同期通信でL1閲覧ウインドウの内容を書き換える
var pseudoAdd = function( com, food_key, code ){
	$.post( "pseudo.cgi", { command:com, food_key:food_key, code:code }, function( data ){
		$( "#LF" ).html( data );

		dlf = true;
		displayBW();
	});
};


// 登録ボタンを押してLFにエディタを表示
var pseudoSave = function( code ){
	var food_name = document.getElementById( "pfood_name" ).value;

	if( food_name != '' ){
		var food_group = document.getElementById( "pfood_group" ).value;
		var class1 = document.getElementById( "pclass1" ).value;
		var class2 = document.getElementById( "pclass2" ).value;
		var class3 = document.getElementById( "pclass3" ).value;
		var tag1 = document.getElementById( "ptag1" ).value;
		var tag2 = document.getElementById( "ptag2" ).value;
		var tag3 = document.getElementById( "ptag3" ).value;
		var tag4 = document.getElementById( "ptag4" ).value;
		var tag5 = document.getElementById( "ptag5" ).value;
		var food_weight = document.getElementById( "pfood_weight" ).value;

		var REFUSE = document.getElementById( "pREFUSE" ).value;
		var ENERC = document.getElementById( "pENERC" ).value;
		var ENERC_KCAL = document.getElementById( "pENERC_KCAL" ).value;
		var WATER = document.getElementById( "pWATER" ).value;

		var PROTCAA = document.getElementById( "pPROTCAA" ).value;
		var PROT = document.getElementById( "pPROT" ).value;
		var PROTV = document.getElementById( "pPROTV" ).value;
		var FAT = document.getElementById( "pFAT" ).value;
		var FATV = document.getElementById( "pFATV" ).value;
		var FATNLEA = document.getElementById( "pFATNLEA" ).value;
		var CHOLE = document.getElementById( "pCHOLE" ).value;
		var CHOAVLM = document.getElementById( "pCHOAVLM" ).value;
		var CHOAVL = document.getElementById( "pCHOAVL" ).value;
		var CHOAVLDF = document.getElementById( "pCHOAVLDF" ).value;
		var CHOV = document.getElementById( "pCHOV" ).value;
		var FIB = document.getElementById( "pFIB" ).value;
		var CHOCDF = document.getElementById( "pCHOCDF" ).value;
		var OA = document.getElementById( "pOA" ).value;
		var POLYL = document.getElementById( "pPOLYL" ).value;

		var ASH = document.getElementById( "pASH" ).value;
		var NA = document.getElementById( "pNA" ).value;
		var K = document.getElementById( "pK" ).value;
		var CA = document.getElementById( "pCA" ).value;
		var MG = document.getElementById( "pMG" ).value;
		var P = document.getElementById( "pP" ).value;
		var FE = document.getElementById( "pFE" ).value;
		var ZN = document.getElementById( "pZN" ).value;
		var CU = document.getElementById( "pCU" ).value;
		var MN = document.getElementById( "pMN" ).value;
		var ID = document.getElementById( "pID" ).value;
		var SE = document.getElementById( "pSE" ).value;
		var CR = document.getElementById( "pCR" ).value;
		var MO = document.getElementById( "pMO" ).value;

		var RETOL = document.getElementById( "pRETOL" ).value;
		var CARTA = document.getElementById( "pCARTA" ).value;
		var CARTB = document.getElementById( "pCARTB" ).value;
		var CRYPXB = document.getElementById( "pCRYPXB" ).value;
		var CARTBEQ = document.getElementById( "pCARTBEQ" ).value;
		var VITA_RAE = document.getElementById( "pVITA_RAE" ).value;
		var VITD = document.getElementById( "pVITD" ).value;
		var TOCPHA = document.getElementById( "pTOCPHA" ).value;
		var TOCPHB = document.getElementById( "pTOCPHB" ).value;
		var TOCPHG = document.getElementById( "pTOCPHG" ).value;
		var TOCPHD = document.getElementById( "pTOCPHD" ).value;
		var VITK = document.getElementById( "pVITK" ).value;

		var THIA = document.getElementById( "pTHIA" ).value;
		var RIBF = document.getElementById( "pRIBF" ).value;
		var NIA = document.getElementById( "pNIA" ).value;
		var NE = document.getElementById( "pNE" ).value;
		var VITB6A = document.getElementById( "pVITB6A" ).value;
		var VITB12 = document.getElementById( "pVITB12" ).value;
		var FOL = document.getElementById( "pFOL" ).value;
		var PANTAC = document.getElementById( "pPANTAC" ).value;
		var BIOT = document.getElementById( "pBIOT" ).value;
		var VITC = document.getElementById( "pVITC" ).value;

		var ALC = document.getElementById( "pALC" ).value;
		var NACL_EQ = document.getElementById( "pNACL_EQ" ).value;
		var Notice = document.getElementById( "pNotice" ).value;

		var FASAT = document.getElementById( "pFASAT" ).value;
		var FAMS = document.getElementById( "pFAMS" ).value;
		var FAPU = document.getElementById( "pFAPU" ).value;
		var FAPUN3 = document.getElementById( "pFAPUN3" ).value;
		var FAPUN6 = document.getElementById( "pFAPUN6" ).value;

		var FIBTG = document.getElementById( "pFIBTG" ).value;
		var FIBSOL = document.getElementById( "pFIBSOL" ).value;
		var FIBINS = document.getElementById( "pFIBINS" ).value;
		var FIBTDF = document.getElementById( "pFIBTDF" ).value;
		var FIBSDFS = document.getElementById( "pFIBSDFS" ).value;
		var FIBSDFP = document.getElementById( "pFIBSDFP" ).value;
		var FIBIDF = document.getElementById( "pFIBIDF" ).value;
		var STARES = document.getElementById( "pSTARES" ).value;

		$.post( "pseudo.cgi", {
			command:'save', code:code, food_name:food_name, food_group:food_group, food_weight:food_weight,
			class1:class1, class2:class2, class3:class3, tag1:tag1, tag2:tag2, tag3:tag3, tag4:tag4, tag5:tag5,
			REFUSE:REFUSE,  ENERC:ENERC, ENERC_KCAL:ENERC_KCAL, WATER:WATER,
			PROTCAA:PROTCAA, PROT:PROT, PROTV:PROTV, FATNLEA:FATNLEA, CHOLE:CHOLE, FAT:FAT, FATV:FATV, CHOAVLM:CHOAVLM, CHOAVL:CHOAVL, CHOAVLDF:CHOAVLDF, CHOV:CHOV, FIB:FIB, POLYL:POLYL, CHOCDF:CHOCDF, OA:OA,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIA:THIA, RIBF:RIBF, NIA:NIA, NE:NE, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			ALC:ALC, NACL_EQ:NACL_EQ, Notice:Notice,
			FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, FAPUN3:FAPUN3, FAPUN6:FAPUN6,
			FIBTG:FIBTG, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTDF:FIBTDF, FIBSDFS:FIBSDFS, FIBSDFP:FIBSDFP, FIBIDF:FIBIDF, STARES:STARES
		}, function( data ){
			$( "#LF" ).html( data );
			displayVIDEO( food_name + ' saved' );
		});
	} else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};

// 削除ボタンを押したときに非同期通信でLFの内容を書き換える
var pseudoDelete = function( code ){
	$.post( "pseudo.cgi", { command:'delete', code:code }, function( data ){
		$( "#LF" ).html( data );

		dlf = false;
		displayBW();
		displayVIDEO( code + ' deleted' );
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Bookshelf /////////////////////////////////////////////////////////////////////////

var bookOpen = function( url, depth ){
	dline = false;
	displayBW();

	closeBroseWindows( depth );
	$.ajax({ url:url, type:'GET', dataType:'html', success:function( data ){ $( "#L" + depth ).html( data ); }});
	document.getElementById( "L" + depth ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Memory list ///////////////////////////////////////////////////////////////////////

const initMemoryList = function(){
	$.post( "memory-list.cgi", { command:'init' }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};

// Save New category
const newCategory = function(){
	const category = document.getElementById( 'new_category' ).value;
	if( category != '' ){
		$.post( "memory-list.cgi", { command:'save', category:category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( 'Category name!(>_<)' );
	}
};

// Delete category
const deleteCategory = function( category, delete_check_no ){
	if( document.getElementById( delete_check_no ).checked ){
		$.post( "memory-list.cgi", { command:'delete', category:category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( 'Check!' );
	}
};

// Change category name
const changeCategory = function( category ){
	let new_category = document.getElementById( category ).value;
	if( category != '' ){
		$.post( "memory-list.cgi", { command:'change', category:category, new_category:new_category }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVIDEO( 'Category name!(>_<)' );
	}
};

// List each pointer
const listPointers = function( category ){
	$.post( "memory-list.cgi", { command:'pointers', category:category }, function( data ){ $( "#L1" ).html( data );});
};

/////////////////////////////////////////////////////////////////////////////////
// Memory edit///////////////////////////////////////////////////////////////////////

// Add new memory
const newMemory = function( category_, pointer, mode ){
	let category = category_
	if( category_ == '' && mode == 'refer' ){ category = document.getElementById( 'ref_new_categoly' ).value; }
	$.post( "memory-edit.cgi", { command:'new', category:category, pointer:pointer, mode:mode, depth:2 }, function( data ){
		$( "#LF" ).html( data );
		pushBW();
		flashBW();
		dlf = true;
		displayBW();
	});
};

const editMemory = function( code, mode ){
	$.post( "memory-edit.cgi", { command:'edit', code:code, mode:mode, depth:2 }, function( data ){
		$( "#LF" ).html( data );
		pushBW();
		flashBW();
		dlf = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Memory ///////////////////////////////////////////////////////////////////////

// Open memory
const memoryOpen = function( code ){
	$.post( "memory.cgi", { command:'refer', code, depth:2 }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		pushBW();
		displayBW();
	});
};


// Open memory code
//const memoryOpenCode = function( code ){
//	$.post( "memory.cgi", { command:'refer_code', code, depth:2 }, function( data ){
//		$( "#L2" ).html( data );
//
//		dl2 = true;
//		pushBW();
//		displayBW();
//	});
//};


// Open memory link
const memoryOpenLink = function( words, depth ){
	$.post( "memory.cgi", { command:'refer', words:words, depth:depth }, function( data ){
		$( "#L" + depth ).html( data );
		displayVIDEO( depth );
		switch( depth ){
			case "2":
				dl2 = true;
				break;
			case "3":
				dl3 = true;
				break;
			case "4":
				dl4 = true;
				break;
			case "5":
				dl5 = true;
				break;
			default:
				flashBW();
				dl1 = true;
		}
		pushBW();
		displayBW();

		words = document.getElementById( "words" ).value = words;
		qcate = document.getElementById( "qcate" ).value = 2;
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Meta data //////////////////////////////////////////////////////////////////////////

var metaDisplay = function( com ){
	$.post( "meta.cgi", { command:com }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Proprty //////////////////////////////////////////////////////////////////////////

// Display config menu
var configInit = function(){
	flashBW();
	$.post( "config.cgi", { mod:'menu' }, function( data ){
		$( "#LINE" ).html( data );
		dline = true;
		displayBW();
	});
	$.post( "config.cgi", { mod:'' }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		displayBW();
	});
};

// Display config form
var configForm = function( mod ){
	$.post( "config.cgi", { mod:mod }, function( data ){ $( "#L1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Modal Photo viewer //////////////////////////////////////////////////////////////////////////

const modalPhotoOn = function( code ){
	$.post( "photo.cgi", { command:'modal', code:code }, function( data ){
		$( '#MODAL' ).html( data );
	});
};

////////////////////////////////////////////////////////////////////////////////////////
// Chopping boad interface////////////////////////////////////////////////////////////////////////

// Add food into sum, and reload CB counter
const addingCB = function( fn, weight_id, food_name ){

	displayVIDEO( weight_id );
	if( weight_id != '' ){
		var weight = document.getElementById( weight_id ).value;
	}
	$.post( "cboardm.cgi", { food_no:fn, food_weight:weight, mode:'add' }, function( data ){
		$( "#CBN" ).html( data );
		if( fn != '' ){ displayVIDEO( '+' + food_name ); }

		if( weight_id == 'weight_sub' ){
			initCB( 'init' );

			flashBW();
			dl1 = true;
			displayBW();
		}
	});

	refreshCBN();
};


// Only reload CB number
const refreshCBN = function(){
	$.post( "cboardm.cgi", { mode:'refresh' }, function( data ){ $( "#CBN" ).html( data );});
};


////////////////////////////////////////////////////////////////////////////////////////
// Chopping boad ////////////////////////////////////////////////////////////////////////

// Display CB sum
const initCB = function( com, code, recipe_user ){
	if( com == 'reload' ){
		$.post( "cboard.cgi", { command:'reload', code:code }, function( data ){
			$( "#L1" ).html( data );
		});
	}else{
		$.post( "cboard.cgi", { command:com, code:code, recipe_user:recipe_user }, function( data ){
			$( "#L1" ).html( data );

			flashBW();
			dl1 = true;
			displayBW();
			setTimeout( refreshCBN(), 1000 );
		});
	}
};

// Exchange food in sum
const changingCB = function( fn, base_fn, weight ){
	if( fn !='' ){
		$.post( "cboardm.cgi", { food_no:fn, food_weight:weight, base_fn:base_fn, mode:'change' }, function( data ){
			$( "#CBN" ).html( data );
			displayREC();

			$.post( "#{script}.cgi", { command:'refresh', code:'' }, function( data ){
				$( "#L1" ).html( data );

				flashBW();
				dl1 = true;
				displayBW();
			});
		});
	}
};



////////////////////////////////////////////////////////////////////////////////
// Recipe editor ////////////////////////////////////////////////////////////////////////

const recipeEdit = function( com, code ){
	$.post( "recipe.cgi", { command:com, code:code }, function( data ){
		$( "#L2" ).html( data );
		dl2 = true;
		displayBW();
	});
};


////////////////////////////////////////////////////////////////////////////////////
// Recipe list ////////////////////////////////////////////////////////////////////////

const recipeList = function( com ){
	$.post( "recipel.cgi", { command:com }, function( data ){
		$( "#L1" ).html( data );
		if( com == 'reset'){ document.getElementById( "words" ).value = ''; }

		flashBW();
		dl1 = true;
		displayBW();
	});
};


///////////////////////////////////////////////////////////////////////////////////
// 成分計算 ////////////////////////////////////////////////////////////////////////

// まな板の成分計算表ボタンを押してL2にリストを表示
var calcView = function( code ){
	$.post( "calc.cgi", { command:'view', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 成分計算表の再計算ボタンを押してL2にリストを表示
var recalcView = function( code ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "calc.cgi", { command:'view', code:code, palette:palette, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Recalc' );
	});
};


///////////////////////////////////////////////////////////////////////////////////
// 原価計算 ////////////////////////////////////////////////////////////////////////

// まな板の原価計算表ボタンを押してL2にリストを表示
var priceView = function( code ){
	$.post( "price.cgi", { command:'view', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 原価計算表の購入量変更でL2に原価表を更新
var changeFV = function( code, fvid, food_no ){
	var food_volume = document.getElementById( fvid ).value;
	$.post( "price.cgi", { command:'changeFV', code:code, food_volume:food_volume, food_no:food_no }, function( data ){ $( "#L2" ).html( data );});
};

// 原価計算表の支払金額変更でL2に原価表を更新
var changeFP = function( code, fpid, food_no ){
	var food_price = document.getElementById( fpid ).value;
	$.post( "price.cgi", { command:'changeFP', code:code, food_price:food_price, food_no:food_no }, function( data ){ $( "#L2" ).html( data );});
};

// 原価計算表のマスター価格を適用してL2に原価表を更新
var pricemAdpt = function( code ){
	$.post( "price.cgi", { command:'adpt_master', code:code }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'マスター価格を適用' );
	});
};

// 原価計算表のマスター価格登録（でL2に原価表を更新）
var pricemReg = function( code ){
	$.post( "price.cgi", { command:'reg_master', code:code }, function( data ){
//		$( "#L2" ).html( data );
		displayVIDEO( 'マスター価格に登録' );
	});
};

// 原価計算表の価格を元にレシピの価格区分を変更
var recipeRef = function( code ){
	$.post( "price.cgi", { command:'ref_recipe', code:code }, function( data ){
//		$( "#L2" ).html( data );
		displayVIDEO( '価格区分へ反映' );
	});
};

// 原価計算表の初期化ボタンでL2に原価表を更新
var clearCT = function( code ){
	if( document.getElementById( "clearCT_check" ).checked ){
		$.post( "price.cgi", { command:'clearCT', code:code }, function( data ){ $( "#L2" ).html( data );});
	}else{
		displayVIDEO( '(>_<) check!' );
	}
};

///////////////////////////////////////////////////////////////////////////////////
// Lucky star input ////////////////////////////////////////////////////////////////////////

// Lucky☆入力ボタンを押してL2に入力画面を表示、そしてL1を非表示にする
const luckyInput = function(){
	$.post( "lucky.cgi", { command:'init' }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};


///////////////////////////////////////////////////////////////////////////////////
// Foodize ////////////////////////////////////////////////////////////////////////

// 成分計算表の食品化ボタンを押してL3に擬似食品フォームを表示
var Pseudo_R2F = function( code ){
	$.post( "pseudo_r2f.cgi", { command:'form', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 食品化フォームの保存ボタンを押して保存してL3を消す。
var savePseudo_R2F = function( code ){
	var food_name = document.getElementById( "r2ffood_name" ).value;
	if( food_name != '' ){

		var food_group = document.getElementById( "r2ffood_group" ).value;
		var class1 = document.getElementById( "r2fclass1" ).value;
		var class2 = document.getElementById( "r2fclass2" ).value;
		var class3 = document.getElementById( "r2fclass3" ).value;
		var tag1 = document.getElementById( "r2ftag1" ).value;
		var tag2 = document.getElementById( "r2ftag2" ).value;
		var tag3 = document.getElementById( "r2ftag3" ).value;
		var tag4 = document.getElementById( "r2ftag4" ).value;
		var tag5 = document.getElementById( "r2ftag5" ).value;

		$.post( "pseudo_r2f.cgi", {
			command:'save', code:code,
			food_name:food_name, food_group:food_group, class1:class1, class2:class2, class3:class3, tag1:tag1,
			tag2:tag2, tag3:tag3, tag4:tag4, tag5:tag5
		}, function( data ){
//			$( "#L2" ).html( data );
			displayVIDEO( 'Foodized' );

			dl2 = false;
			displayBW();
		});
	}else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};

///////////////////////////////////////////////////////////////////////////////////
// Print selector /////////////////////////////////////////////////////////////////

const print_templateSelect = function( code ){
	$.post( "print.cgi", { command:'init', code:code }, function( data ){
		$( "#L2" ).html( data );
		$( '#modal_tip' ).modal( 'hide' );

		flashBW();
		dl2 = true;
		displayBW();
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Set menu ////////////////////////////////////////////////////////////////////////

// 献立追加ボタンを押してmealにレシピを追加して、まな献立カウンタを増やす
var addingMeal = function( recipe_code, recipe_name ){
	$.post( "mealm.cgi", { recipe_code:recipe_code }, function( data ){
		$( "#MBN" ).html( data );
		$( '#modal_tip' ).modal( 'hide' );

		if( recipe_code != '' ){ displayVIDEO( '+' + recipe_name); }
	});
};


// 献立ボタンを押してL1にリストを表示
var initMeal = function( com, code ){
	$.post( "meal.cgi", { command:com, code:code }, function( data ){
		$( "#L1" ).html( data );
		flashBW();
		dl1 = true;
		displayBW();
	});
};

// 献立クリアボタンを押してL1にリストを更新、そしてまな献立カウンターの更新
var clear_meal = function( order, code ){
	if( order == 'all'){
		if( document.getElementById( 'meal_all_check' ).checked ){
			$.post( "meal.cgi", { command:'clear', order:'all', code:code }, function( data ){
				$( "#L1" ).html( data );
				addingMeal( '' );

				displayVIDEO( 'Menu cleared' );
				flashBW();
				dl1 = true;
				displayBW();
			});
		} else{
			displayVIDEO( 'Check! (>_<)' );
		}
	} else{
		$.post( "meal.cgi", { command:'clear', order:order, code:code }, function( data ){
			$( "#L1" ).html( data );
			addingMeal( '' );
		});
	}
};


// 献立上ボタンを押してL1に献立リストを更新
var upper_meal = function( order, code ){
	$.post( "meal.cgi", { command:'upper', order:order, code:code }, function( data ){ $( "#L1" ).html( data );});
};


// 献立下ボタンを押してL1に献立リストを更新
var lower_meal = function( order, code ){
	$.post( "meal.cgi", { command:'lower', order:order, code:code }, function( data ){ $( "#L1" ).html( data );});
};

////////////////////////////////////////////////////////////////////////////////
// セットメニュー ////////////////////////////////////////////////////////////////////////

// 献立編集のレシピボタンを押してL2にレシピを表示
var menuEdit = function( com, code ){
	$.post( "menu.cgi", { command:com, code:code }, function( data ){
		$( "#L2" ).html( data );
		dl2 = true;
		displayBW();
	});
	$.post( "photo.cgi", { command:'view_series', code:code, base:'menu' }, function( data ){
		$( "#LM" ).html( data )
		dlm = true;
		displayBW();
	});
};


// メニュー編集の保存ボタンを押してレシピを保存、そしてL2にリストを再表示
var menuSave = function( code ){
	var menu_name = document.getElementById( "menu_name" ).value;
	if( menu_name == '' ){
		displayVIDEO( 'Menu name! (>_<)' );
	}
	else{
		if( document.getElementById( "public" ).checked ){ var public = 1 }
		if( document.getElementById( "protect" ).checked ){ var protect = 1 }
		var label = document.getElementById( "label" ).value;
		var new_label = document.getElementById( "new_label" ).value;
		var memo = document.getElementById( "memo" ).value;

		$.post( "menu.cgi", { command:'save', code:code, menu_name:menu_name, public:public, protect:protect, label:label, new_label:new_label, memo:memo }, function( data ){
			$( "#L2" ).html( data );
			$.post( "meal.cgi", { command:'init', code:code }, function( data ){$( '#L1' ).html( data );});
			displayVIDEO( menu_name );
		});
	}
};


// Copying lebel to new label
var copyLabel = function(){
	document.getElementById( "new_label" ).value = document.getElementById( "label" ).value;
};


// Changing label set
var switchLabelset = function( normal_label_c, school_label_c ){
	var label_status = document.getElementById( 'normal_label0' ).style.display;
	if( school_label_c > 0){
		if( label_status == 'inline' ){
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label' + i ).style.display = 'none';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label' + i ).style.display = 'inline';
			}
			document.getElementById( 'label' ).selectedIndex = normal_label_c + 1;
		}else{
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label' + i ).style.display = 'inline';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label' + i ).style.display = 'none';
			}
			document.getElementById( 'label' ).selectedIndex = 0;
		}
	}
}

////////////////////////////////////////////////////////////////////////////////////
// Set menu list ////////////////////////////////////////////////////////////////////////

// まな板のレシピ読み込みボタンを押してL1に献立リストを表示
var menuList = function( page ){
	$.post( "menul.cgi", { command:'view', page:page }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
		dl1 = true;
		displayBW();
	});
};


// まな板のレシピ読み込みボタンを押してL1に献立リストを表示
var menuList2 = function( page ){
	var range = document.getElementById( "range" ).value;
	var label = document.getElementById( "label_list" ).value;
	$.post( "menul.cgi", { command:'view2', page:page, range:range, label:label }, function( data ){ $( "#L1" ).html( data );});
};


// まな板の削除ボタンを押してレシピを削除し、L1にリストを再表示
var menuDelete = function( code, menu_name ){
	if( document.getElementById( code ).checked ){
		$.post( "menul.cgi", { command:'delete', code:code }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( menu_name );
		});
	} else{
		displayVIDEO( 'Check! (>_<)' );
	}
};


// まな板のインポートボタンを押してレシピをインポートし、L1にリストを再表示
var menuImport = function( code ){
	$.post( "menul.cgi", { command:'import', code:code }, function( data ){
		$( "#L1" ).html( data );
		
		displayVIDEO( code );
	});
};


// Changing label set
var switchLabelsetl = function( normal_label_c, school_label_c ){
	var label_status = document.getElementById( 'normal_label_list0' ).style.display;
	if( school_label_c > 0){
		if( label_status == 'inline' ){
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label_list' + i ).style.display = 'none';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label_list' + i ).style.display = 'inline';
			}
			document.getElementById( 'label_list' ).selectedIndex = normal_label_c + 1;
		}else{
			for( let i = 0; i <= normal_label_c; i++ ){
				document.getElementById( 'normal_label_list' + i ).style.display = 'inline';
			}
			for( let i = 1; i <= school_label_c; i++ ){
				document.getElementById( 'school_label_list' + i ).style.display = 'none';
			}
			document.getElementById( 'label_list' ).selectedIndex = 0;
		}
	}
}

///////////////////////////////////////////////////////////////////////////////////
// 献立の成分計算 ////////////////////////////////////////////////////////////////////////

// 献立の成分計算表ボタンを押してL2にリストを表示
var menuCalcView = function( code ){
	$.post( "menu-calc.cgi", { command:'view', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// 献立の成分計算表の再計算ボタンを押してL2にリストを表示
var menuRecalcView = function( code ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "menu-calc.cgi", { command:'view', code:code, palette:palette, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Recalc' );
	});
};


///////////////////////////////////////////////////////////////////////////////////
// Analysis of menu ////////////////////////////////////////////////////////////////////////

// Analysis of menu
var menuAnalysis = function( code ){
	$.post( "menu-analysis.cgi", { command:'', code:code }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl1 = true;
		dl2 = true;
		displayBW();
	});
};

// Reanalysis of menu
var menuReAnalysis = function( code ){
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "menu-analysis.cgi", { command:'', code:code, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){
		$( "#L2" ).html( data );
		displayVIDEO( 'Reanalysis' );
	});
};

