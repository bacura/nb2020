// Nutorition Browser 2020 core.js 0.2b (2022/11/30)
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

		bookOpen( 'books/about.html', 1 );
		bookOpen( 'books/information.html', 2 );
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
};


// Reopening browse windows
displayBW = function(){
	if( dl1 ){ bwl1.style.display = 'block'; }else{ bwl1.style.display = 'none'; }
	if( dl2 ){ bwl2.style.display = 'block'; }else{ bwl2.style.display = 'none'; }
	if( dl3 ){ bwl3.style.display = 'block'; }else{ bwl3.style.display = 'none'; }
	if( dl4 ){ bwl4.style.display = 'block'; }else{ bwl4.style.display = 'none'; }
	if( dl5 ){ bwl5.style.display = 'block'; }else{ bwl5.style.display = 'none'; }
	if( dlf ){ bwlf.style.display = 'block'; }else{ bwlf.style.display = 'none'; }
	if( dline ){ line.style.display = 'block'; }else{ line.style.display = 'none'; }
};


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
};


// Pulling level status from hide
pullHW = function(){
	dl1 = hl1;
	dl2 = hl2;
	dl3 = hl3;
	dl4 = hl4;
	dl5 = hl5;
	dlf = hlf;
	dline = hline;
};


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
	var fx = function(){
		video.innerHTML = "";
		video.style.display = 'none';
	};
	setTimeout( fx, 2000 );
};


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

/////////////////////////////////////////////////////////////////////////////////
// Account /////////////////////////////////////////////////////////////////////////
// Changing Account
chageAccountM = function(){
	var login_mv = document.getElementById( "login_mv" ).value;
	location.href = "login.cgi?mode=family" + "&login_mv=" + login_mv;
};


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


// Display foods on BWL5
var summonL5 = function( key, direct ){
	if( direct > 0 ){ closeBroseWindows( direct ); }
	$.get( "square.cgi", { channel:"fctb_l5", food_key:key }, function( data ){ $( "#L5" ).html( data );});
	dl5 = true;
	dlf = false;
	displayBW();
};


// Changing weight of food
var changeWeight = function( key, fn ){
	var fraction_mode = document.getElementById( "fraction" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.get( "square.cgi", { channel:"fctb_l5", food_key:key, frct_mode:fraction_mode, food_weight:weight }, function( data ){ $( "#L5" ).html( data );});
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
var detailPage = function( dir, sid ){
	var fraction_mode = document.getElementById( "detail_fraction" ).value;
	var food_weight = document.getElementById( "detail_volume" ).value;
	var selectu = document.getElementById( "detail_unit" ).value;
	$.post( "detail.cgi", { dir:dir, sid:sid, frct_mode:fraction_mode, food_weight:food_weight, selectu:selectu }, function( data ){ $( "#LF" ).html( data );});
};

// 詳細画面のページボタンを押したらL5閲覧ウインドウの内容を書き換える。
var detailReturn = function(){
	pullHW();
	displayBW();
};


/////////////////////////////////////////////////////////////////////////////////
// Referencing /////////////////////////////////////////////////////////////////////////

// Disply results
var search = function(){
	var words = document.getElementById( "words" ).value;
	var qcate = document.getElementById( "qcate" ).value;
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
			$.post( "memory.cgi", { command:'refer', pointer:words, depth:1 }, function( data ){
				$( "#L1" ).html( data );
		 		dl1 = true;
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

	displayVIDEO( 'Copied' );
};


/////////////////////////////////////////////////////////////////////////////////
// history /////////////////////////////////////////////////////////////////////////

// Display history
var historyInit = function(){
	flashBW();
	$.post( "history.cgi", { command:'menu' }, function( data ){
		$( "#LINE" ).html( data );
		dline = true;
		displayBW();
	});
	$.post( "history.cgi", { command:'sub', sub_fg:'init' }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		displayBW();
	});
	pushBW();


};

var historySub = function( sub_fg ){
	$.post( "history.cgi", { command:'sub', sub_fg:sub_fg }, function( data ){ $( "#L1" ).html( data );});
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

// Display Bookshelf
var bookOpen = function( url, depth ){
	dline = false;
	displayBW();

	closeBroseWindows( depth );
	$.ajax({ url:url, type:'GET', dataType:'html', success:function( data ){ $( "#L" + depth ).html( data ); }});
	document.getElementById( "L" + depth ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Memory ///////////////////////////////////////////////////////////////////////

// Memory init
var initMemory_ = function(){
	$.post( "memory.cgi", { command:'init' }, function( data ){
		$( "#L2" ).html( data );

		flashBW();
		dl2 = true;
		displayBW();
	});
};


// List each pointer
var listPointer = function( category ){
	$.post( "memory.cgi", { command:'list_pointer', category:category }, function( data ){
		$( "#L2" ).html( data );

		dl2 = true;
		displayBW();
	});
};


// Open memory link
var memoryOpenLink = function( pointer, depth ){
	$.post( "memory.cgi", { command:'refer', pointer:pointer, depth:depth }, function( data ){
		$( "#L" + depth ).html( data );
		if( depth == '1' ){ closeBroseWindows( 1 ); }
		document.getElementById( "L" + depth ).style.display = 'block';

		words = document.getElementById( "words" ).value = pointer;
		qcate = document.getElementById( "qcate" ).value = 2;
	});
};


// New pointer form
var newPMemory = function( category, pointer, post_process ){
	$.post( "memory.cgi", { command:'new_pointer', category:category, pointer:pointer, post_process:post_process }, function( data ){
		$( "#LF" ).html( data );

		if( post_process == 'front'){ document.getElementById( "L2" ).style.display = 'none'; }
		document.getElementById( "LF" ).style.display = 'block';
	});
};

/////////////////////////////////////////////////////////////////////////////////
// Meta data //////////////////////////////////////////////////////////////////////////

// Display meta data
var metaDisplay = function( com ){
	$.post( "meta.cgi", { command:com }, function( data ){
		$( "#L3" ).html( data );

		dl3 = true;
		displayBW();
	});
};


/////////////////////////////////////////////////////////////////////////////////
// Proprty //////////////////////////////////////////////////////////////////////////

// Display config menu
var configInit = function(){
	flashBW();
	$.post( "config.cgi", { mod:'' }, function( data ){
		$( "#LINE" ).html( data );
		dline = true;
		displayBW();
	});
	$.post( "config.cgi", { mod:'account' }, function( data ){
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
// Photo //////////////////////////////////////////////////////////////////////////

// レシピ編集の写真をアップロードして保存、そしてL3に写真を再表示
var photoSave = function( code, form, base ){
	form_data = new FormData( $( form )[0] );
	form_data.append( 'command', 'upload' );
	form_data.append( 'code', code );
	form_data.append( 'base', base );

	$.ajax( "photo.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ $( '#L3' ).html( data ); }
		}
	);
};


// delete photo from media db
var photoDel = function( code, mcode, base ){
	$.post( "photo.cgi", { command:'delete', code:code, mcode:mcode, base:base }, function( data ){ $( '#L3' ).html( data );});
};
