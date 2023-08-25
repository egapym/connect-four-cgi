nextcolor="#eeeeee";       //変更後の色(Default)
//----------------------
function tablegetclass(cl,ta){
var class_obj=new Array();
var ccount=0;
tag_obj=document.getElementsByTagName(ta);

  for(i=0;i<tag_obj.length;i++){
    var clas=tag_obj[i].className;
      if(clas.indexOf(" ") != -1){
      clas=clas.split(" ");
        for(j=0;j<clas.length;j++){
         var clas1=(clas[j].indexOf(":") != -1)?clas[j].split(":")[0]:clas[j];
         var clas2=(clas[j].indexOf(":") != -1)?clas[j].split(":")[1]:"";
          if(clas1 == cl){
            class_obj[ccount]=tag_obj[i];
            class_obj[ccount].para=(clas2)?clas2:"";
            ccount++;
            break;
          }
       }
      }else{
         var clas1=(clas.indexOf(":") != -1)?clas.split(":")[0]:clas;
         var clas2=(clas.indexOf(":") != -1)?clas.split(":")[1]:"";
          if(clas1 == cl){
            class_obj[ccount]=tag_obj[i];
            class_obj[ccount].para=(clas2)?clas2:"";
            ccount++;
          }
      }
  }
return class_obj;
}

//--------------------
//--------------------

/*
class="rowcolor"
*/

rowtable_name="rowcolor"     //行色変更適応名

function table_row(){
taobj=tablegetclass(rowtable_name,"TABLE");

  for(i=0; i<taobj.length;i++){
     var nextscolor=(taobj[i].para)? taobj[i].para:nextcolor;

   var tobj=taobj[i].tBodies[0];
     for (j=0; j<tobj.rows.length;j++){
       tobj.rows[j].nc=nextscolor;
       tobj.rows[j].onmouseover=function(){this.fc=this.style.backgroundColor;this.style.backgroundColor=this.nc};
       tobj.rows[j].onmouseout=function(){this.style.backgroundColor=this.fc};
     }
  }
}

//--------------------
//--------------------

/*
class="cellcolor"
*/

celltable_name="cellcolor"    //列色変更適応名

function table_cell(){
cell_taobj=tablegetclass(celltable_name,"TABLE");

  for(var i=0; i<cell_taobj.length;i++){
        var nextscolor = cell_taobj[i].para?cell_taobj[i].para:nextcolor;
   var tobj=cell_taobj[i].tBodies[0];
   tobj.nc=nextscolor;
     for (var j=0; j<tobj.rows.length;j++){
             for (var k=0; k<tobj.rows[j].cells.length;k++){
                    tobj.rows[j].cells[k].fc=tobj.rows[j].cells[k].style.backgroundColor;
                    tobj.rows[j].cells[k].cel=k;
                    tobj.rows[j].cells[k].onmouseover=function(){cell_set(this,this.cel)};
                    tobj.rows[j].cells[k].onmouseout=function(){cell_reset(this,this.cel)};
             }
     }
  }
}

function cell_set(t,c){
   var tobj=t.parentNode.parentNode;
     for (var j=0; j<tobj.rows.length;j++)
                    tobj.rows[j].cells[c].style.backgroundColor=tobj.nc;
}

function cell_reset(t,c){
   var tobj=t.parentNode.parentNode;
     for (var j=0; j<tobj.rows.length;j++)
                    tobj.rows[j].cells[c].style.backgroundColor=tobj.rows[j].cells[c].fc;
}


//---------------------
//---------------------

movecell_name="cellmove"     //入れ替え適応名

nextmcolor="#eeeeee";

function tablecell_move(){

mtobj=tablegetclass(movecell_name,"TABLE");

  for(var i=0; i<mtobj.length;i++){
        var nextcolor = (mtobj[i].para)?mtobj[i].para:nextmcolor;
       mtobj[i].onselectstart = function(){return false};
       mtobj[i].style.cursor = "pointer";
       var mtaobj=mtobj[i].tBodies[0];
       mtaobj.ncc=nextcolor;
     for (var j=0; j<mtaobj.rows.length;j++){
              for (var k=0; k<mtaobj.rows[j].cells.length;k++){

  if(mtaobj.rows[j].cells[k].bgColor==""){
       var stcolor=mtaobj.rows[j].cells[k].style.backgroundColor;
       if(stcolor && stcolor.indexOf("rgb")!=-1)
         stcolor=rgbcolor(stcolor);
       mtaobj.rows[j].cells[k].bgColor=stcolor;
  }
       mtaobj.rows[j].cells[k].cel=k;
       mtaobj.rows[j].cells[k].onmousedown=function(){cellset(this,this.cel);};
       mtaobj.rows[j].cells[k].onmouseup=function(){cellchange(this,this.cel);};
             }
     }
  }
}

function rgbcolor(rgb){
var s = rgb.split(",");
var rgb_16="#";
  for (var i=0; i<s.length;i++){
if(!i)s[i]=s[i].substring(4);
      temp=parseInt(s[i]);
      temp_rgb=temp.toString(16);
      if(temp_rgb.length==1)temp_rgb="0"+temp_rgb;
      rgb_16+=temp_rgb;
  }
return rgb_16;

}

var tempcell="";
function cellset(cel,celno){
  var taparpar=cel.parentNode.parentNode;

     for (var i=0; i<taparpar.rows.length;i++){
        for (var j=0; j<taparpar.rows[i].cells.length;j++){
            taparpar.rows[i].cells[j].style.backgroundColor="";
            if(j==celno)taparpar.rows[i].cells[j].style.backgroundColor=taparpar.ncc;
        }
     }

tempcell=celno;
}

function cellchange(cel,celno){
  var taparpar=cel.parentNode.parentNode;
     for (var i=0; i<taparpar.rows.length;i++){
        for (var j=0; j<taparpar.rows[i].cells.length;j++){
            taparpar.rows[i].cells[j].style.backgroundColor="";
        }
     }

if(tempcell != "0" && !tempcell)return;
    if(taparpar.focus)taparpar.focus();

if(cel && tempcell != celno){

     for (var i=0; i<taparpar.rows.length;i++){
        var temp2=taparpar.rows[i].cells[celno].cloneNode(true);
        var temp1=taparpar.rows[i].cells[tempcell].cloneNode(true);
        pot = taparpar.rows[i].replaceChild(temp1,taparpar.rows[i].cells[celno]);
        pot2 = taparpar.rows[i].replaceChild(temp2,taparpar.rows[i].cells[tempcell]);
     }
}

    for (i=0; i<taparpar.rows.length;i++){
              for (var j=0; j<taparpar.rows[i].cells.length;j++){
       taparpar.rows[i].cells[j].cel=j;
       taparpar.rows[i].cells[j].onmousedown=function(){cellset(this,this.cel);};
       taparpar.rows[i].cells[j].onmouseup=function(){cellchange(this,this.cel);};
       taparpar.rows[i].cells[j].style.backgroundColor="";
             }
     }
tempcell="";
}

//---------------------
//---------------------

moverow_name="rowmove"     //入れ替え適応名

function tablerow_move(){

mtobj=tablegetclass(moverow_name,"TABLE");

  for(var i=0; i<mtobj.length;i++){
        var nextcolor = (mtobj[i].para)?mtobj[i].para:nextmcolor;
       mtobj[i].onselectstart = function(){return false};
       mtobj[i].style.cursor = "pointer";
       var mtaobj=mtobj[i].tBodies[0];
       mtaobj.nc=nextcolor;
     for (var j=0; j<mtaobj.rows.length;j++){

  if(mtaobj.rows[j].bgColor==""){
       var stcolor=mtaobj.rows[j].style.backgroundColor;
       if(stcolor && stcolor.indexOf("rgb")!=-1)
         stcolor=rgbcolor(stcolor);
       mtaobj.rows[j].bgColor=stcolor;
  }
       mtaobj.rows[j].onmousedown=function(){rowset(this);};
       mtaobj.rows[j].onmouseup=function(){rowchange(this);};
     }
  }
}

var temprow="";
function rowset(ro){
  var tapar=ro.parentNode;

     for (var i=0; i<tapar.rows.length;i++)
      tapar.rows[i].style.backgroundColor="";

ro.style.backgroundColor=tapar.nc;
temprow=ro;

}
function rowchange(ro){
  var tapar=ro.parentNode;
     for (var i=0; i<tapar.rows.length;i++)
      tapar.rows[i].style.backgroundColor="";

if(!temprow)return;
if(temprow.focus)temprow.focus();

if(ro && temprow != ro){

  var temp2=ro.cloneNode(true);
  var temp1=temprow.cloneNode(true);

  pot = tapar.replaceChild(temp1,ro);
  pot2 = tapar.replaceChild(temp2,temprow);

}
     for (var j=0; j<tapar.rows.length;j++){
       tapar.rows[j].onmousedown=function(){rowset(this);};
       tapar.rows[j].onmouseup=function(){rowchange(this);};
       tapar.rows[j].style.backgroundColor="";
     }
temprow="";
}

tmptableload = window.onload;
window.onload= function () {if(tmptableload)tmptableload();table_row();table_cell();tablecell_move();tablerow_move();}
/* himajin.moo.jp */