#!/usr/bin/perl --

use utf8;
use open ":utf8";
$vic = 0;
$draw = 0;

loadForm();        #フォームデータ取り込み

loadData();        #データ処理

printData();        #HTML出力

exit(0);

=pod
#!/usr/bin/perl --
#!C:/Perl64/bin/perl
player_turn : プレイヤーの手番。先手なら常に1、後手なら常に2
next_cpu : この変数が2のページの時、次の順番はCPUである事を示す（つまりプレイヤーの番）、1の時は（cpuの番）

=cut

#====================================================================#データ処理
sub    loadData
{
	my $i;
	my $j;

    if($FORM{'next_cpu'} == 1 || $FORM{'next_cpu'} == 2) {
        $DATA = $FORM{'data'};
        if($FORM{'next_cpu'} eq 2) {    #コンピュータの一手
            $NEXT = "player";
            $FORM{'next_cpu'} = 1;
            $MSG = "プレイヤーの順番です";

#=pod
my $te;

if($FORM{'next_cpu'} == 1){
	if($FORM{'player_turn'} eq 1) {
		 $te = "o";
	}else{
		 $te = "x";
	}
}
if($DATA) {
@list = `timeout 3m ./c/ai $te $DATA`;
if(@list[0] eq ""){ #3分間AIが結果を返さなかった場合、タイムアウト処理を行う
error(1);
}
$DATA = $DATA . @list[0];
}elsif($DATA eq "0"){
@list = `./c/ai $te $DATA`;
$DATA = $DATA . @list[0];
}else{
@list[0] = 5;
$DATA = $DATA . @list[0];
}
#=cut
#$DATA = $DATA . "6";
#@list[0] = "6";
        }
        else {                            #プレイヤーの一手
            $NEXT = "cpu";
            $FORM{'next_cpu'} = 2;
            $MSG = "コンピュータ思考中 ";
        }
    }
    else {                                #ゲームスタート
        $DATA =    "";
        if($FORM{'player_turn'} == 1) {
            $NEXT = "player";
            $FORM{'next_cpu'} = 1;
            $MSG = "プレイヤーの順番です";
        }
        else {
            $NEXT = "cpu";
            $FORM{'next_cpu'} = 2;
            $MSG = "コンピュータ思考中 ";
        }
    }

#盤面
 $ban = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
];

my $count = 1;
my $flag = 0;
my $check_i;
my $check_j;
#===============================棋譜データを元にbanに値を代入する
for($i = 0 ; $i < length($DATA) ; $i++) {
	my $rec = substr($DATA, $i, 1);
		if($rec eq "a"){
           $rec = 10;
        }elsif($rec eq "b"){
           $rec = 11;
        }elsif($rec !~ /^[0-9]+$/){
          error(2);
          }
	for($j = 11; $j >= 0; $j--) {
		if($ban->[$j][$rec] == 0){
		if(length($DATA) == $count){
$check_i = $j;
$check_j = $rec;
				}
			if($count % 2 == 0){
				$ban->[$j][$rec] = 2;
				last
			}else{
				$ban->[$j][$rec] = 1;
				last
			}
		}elsif($j == 0 && $ban->[0][$rec] != 0){
				error(3);
			}
	}
		$count++;
}

#=====================置いた手の判定
	if($DATA) {
		if($FORM{'next_cpu'} == 1){					#コンピュータの置いた手の勝利判定
			if($FORM{'player_turn'} == 1){				#コンピュータ（後手）
				$flag = &check_v($check_i,$check_j,2);
			}else{										#コンピュータ（先手）
				$flag = &check_v($check_i,$check_j,1);
			}
				if($flag == 1){
          if($FORM{'result'} == 1){ #resultに値が定義済である
          $MSG = "コンピュータの勝利です";
          $vic = 1;
          }else{
          &data_result(2);
              print qq(Content-type: text/html; charset=UTF-8\n\n);
        print <<"        END";
            <meta http-equiv="refresh"
             content="0;url=$ENV{'SCRIPT_NAME'}?data=$FORM{'data'}&player_turn=$FORM{'player_turn'}&next_cpu=2&result=1">
        END
        exit(0);
          }
				}elsif(length($DATA) >= 144){
          if($FORM{'result'} == 1){ #resultに値が定義済である
          $MSG = "引き分けです";
          $draw = 1;
          }else{
          &data_result(3);
                        print qq(Content-type: text/html; charset=UTF-8\n\n);
        print <<"        END";
            <meta http-equiv="refresh"
             content="0;url=$ENV{'SCRIPT_NAME'}?data=$FORM{'data'}&player_turn=$FORM{'player_turn'}&next_cpu=2&result=1">
        END
        exit(0);
        }
        }
		}else{										#プレイヤーの置いた手の勝利判定
			if($FORM{'player_turn'} == 1){				#プレイヤー（先手）
				$flag = &check_v($check_i,$check_j,1);
			}else{										#コンピュータ（後手）
				$flag = &check_v($check_i,$check_j,2);
			}
				if($flag == 1){
          if($FORM{'result'} == 1){ #resultに値が定義済である
					$MSG = "プレイヤーの勝利です";
					$vic = 1;
          }else{
          &data_result(1);
          &data_kifu(1);
                                  print qq(Content-type: text/html; charset=UTF-8\n\n);
        print <<"        END";
            <meta http-equiv="refresh"
             content="0;url=$ENV{'SCRIPT_NAME'}?data=$FORM{'data'}&player_turn=$FORM{'player_turn'}&next_cpu=1&result=1">
        END
        exit(0);
        }
			}elsif(length($DATA) >= 144){
          if($FORM{'result'} == 1){ #resultに値が定義済である
          $MSG = "引き分けです";
          $draw = 1;
          }else{
          &eval(3);
                                  print qq(Content-type: text/html; charset=UTF-8\n\n);
        print <<"        END";
            <meta http-equiv="refresh"
             content="0;url=$ENV{'SCRIPT_NAME'}?data=$FORM{'data'}&player_turn=$FORM{'player_turn'}&next_cpu=1&result=1">
        END
        exit(0);
        }
        }
		}
	}

}

#===================================================上下左右コマが並んでいるかの判定
sub    check_v
{
	my $flag=0;
  my $result=0;
my ($check_i, $check_j, $player) = @_;

$flag = &check_LR($check_i, $check_j, $player);
if($flag == 1){
	$result = 1;
}
$flag = &check_UD($check_i, $check_j, $player);
if($flag == 1){
  $result = 1;
}
$flag = &check_LURD($check_i, $check_j, $player);
if($flag == 1){
  $result = 1;
}
$flag = &check_RULD($check_i, $check_j, $player);
if($flag == 1){
  $result = 1;
}

	return $result;
}

sub    check_LR
{
	my    ($i, $j, $x, $check, $flag);
	my ($check_i, $check_j, $player) = @_;
$x = -3;
$check = 0;
$flag = 0;

	if ($check_j - 3 < 0) { #配列の番号がマイナスにならないようにする
		$x = 0 - $check_j;
	}
	for ($i = 0; $i<7; $i++) {
		if ($check_j + $x > 11 || $check_j + $x > $check_j + 3) { #配列の行が11を超えたらループを抜ける
			last;
		}
		if ($ban->[$check_i][$check_j + $x] == $player) { #4回連続で配列の値に1を発見したらリターン
			$check++;
			if ($check == 4) {
				$flag = 1;
$ban->[$check_i][$check_j + $x] = $player + 2;
$ban->[$check_i][$check_j + $x - 1] = $player + 2;
$ban->[$check_i][$check_j + $x - 2] = $player + 2;
$ban->[$check_i][$check_j + $x - 3] = $player + 2;
  for ($j = 0; $j<3; $j++) {
    $x++;
    if($check_j + $x <= 11){
      if($ban->[$check_i][$check_j + $x] == $player){
        $ban->[$check_i][$check_j + $x] = $player + 2;
      }else{
        last;
        }
      }else{
        last;
        }
  }
				return $flag;
			}
		}
		elsif ($ban->[$check_i][$check_j + $x] != $player) { #配列に0を発見したらcheck = 0
			$check = 0;
		}
		$x++;
	}
return $flag;
}

sub    check_UD
{
	my    ($i, $j, $y, $check, $flag);
	my ($check_i, $check_j, $player) = @_;
$y = -3;
$check = 0;
$flag = 0;

	if ($check_i - 3 < 0) { #配列の番号がマイナスにならないようにする
		$y = 0 - $check_i;
	}
	for ($i = 0; $i<7; $i++) {
		if ($check_i + $y > 11 || $check_i + $y > $check_i + 3) { #配列の行が11を超えたらループを抜ける
			last;
		}
		if ($ban->[$check_i + $y][$check_j] == $player) { #4回連続で配列の値に1を発見したらリターン
			$check++;
			if ($check == 4) {
				$flag = 1;
$ban->[$check_i + $y][$check_j] = $player + 2;
$ban->[$check_i + $y - 1][$check_j] = $player + 2;
$ban->[$check_i + $y - 2][$check_j] = $player + 2;
$ban->[$check_i + $y - 3][$check_j] = $player + 2;
				return $flag;
			}
		}
		elsif ($ban->[$check_i + $y][$check_j] != $player) { #配列に0を発見したらcheck = 0
			$check = 0;
		}
		$y++;
	}
return $flag;
}

sub    check_LURD
{
	my    ($i, $j, $x, $y, $check, $flag);
	my ($check_i, $check_j, $player) = @_;
$x = -3;
$y = -3;
$check = 0;
$flag = 0;

	#***駒を置いた場所から左上～右下3マスを調べる***
	while (1) { #調べる配列がマイナスにならないようにする
		if ($check_i + $y < 0 || $check_j + $y < 0) {
			$x++;
			$y++;
		}
		else {
			last;
		}
	}
	for ($i = 0; $i<7; $i++) {
		#調べる配列が11を越える、または調べる範囲を越えた場合
		if ($check_i + $y > 11 || $check_i + $y > $check_i + 3) {
			last;
		}
		if ($check_j + $x > 11 || $check_j + $x > $check_j + 3) {
			last;
		}
		if ($ban->[$check_i + $y][$check_j + $x] == $player || $ban->[$check_i + $y][$check_j + $x] == $player + 2) {
			$check++;
			if ($check == 4) {
				$flag = 1;
$ban->[$check_i + $y][$check_j + $x] = $player + 2;
$ban->[$check_i + $y - 1][$check_j + $x - 1] = $player + 2;
$ban->[$check_i + $y - 2][$check_j + $x - 2] = $player + 2;
$ban->[$check_i + $y - 3][$check_j + $x - 3] = $player + 2;
  for ($j = 0; $j<3; $j++) {
    $x++;
    $y++;
    if($check_i + $y <= 11 && $check_j + $x <= 11){
      if($ban->[$check_i + $y][$check_j + $x] == $player){
        $ban->[$check_i + $y][$check_j + $x] = $player + 2;
      }else{
        last;
        }
      }else{
        last;
        }
  }
				return $flag;
			}
		}
		elsif ($ban->[$check_i + $y][$check_j + $x] != $player) {
			$check = 0;
		}
		$x++;
		$y++;
	}
	return $flag;
}

sub    check_RULD
{
	my    ($i, $j, $x, $y, $check, $flag);
	my ($check_i, $check_j, $player) = @_;
$x = 3;
$y = -3;
$check = 0;
$flag = 0;

	#***駒を置いた場所から左上～右下3マスを調べる***
	while (1) { #調べる配列がマイナスにならないようにする
		if ($check_i + $y < 0 || $check_j + $x > 11) {
			$x--;
			$y++;
		}
		else {
			last;
		}
	}
	for ($i = 0; $i<7; $i++) {
		#調べる配列が11を越える、または調べる範囲を越えた場合
		if ($check_j + $x < 0 || $check_j + $x < $check_j - 3) {
			last;
		}
		if ($check_i + $y > 11 || $check_i + $y > $check_i + 3) {
			last;
		}
		if ($ban->[$check_i + $y][$check_j + $x] == $player || $ban->[$check_i + $y][$check_j + $x] == $player + 2) {
			$check++;
			if ($check == 4) {
				$flag = 1;
$ban->[$check_i + $y][$check_j + $x] = $player + 2;
$ban->[$check_i + $y - 1][$check_j + $x + 1] = $player + 2;
$ban->[$check_i + $y - 2][$check_j + $x + 2] = $player + 2;
$ban->[$check_i + $y - 3][$check_j + $x + 3] = $player + 2;
  for ($j = 0; $j<3; $j++) {
    $x--;
    $y++;
    if($check_i + $y <= 11 && $check_j + $x >= 0){
      if($ban->[$check_i + $y][$check_j + $x] == $player){
        $ban->[$check_i + $y][$check_j + $x] = $player + 2;
      }else{
        last;
        }
      }else{
        last;
        }
  }
				return $flag;
			}
		}
		elsif ($ban->[$check_i + $y][$check_j + $x] != $player) {
			$check = 0;
		}
		$x--;
		$y++;
	}
	return $flag;

}

#====================================================================HTML出力
sub    printData
{
my $i;

    if($FORM{'player_turn'} eq "1") {
        $PLAYER    = "●";
        $CPU    = "<font color=\"#ffffff\">●</font>";
    }
    else {
        $PLAYER    = "<font color=\"#ffffff\">●</font>";
        $CPU    = "●";
    }
    print qq(Content-type: text/html; charset=UTF-8\n\n);

    print <<"    END";
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <script src="../js/Hitable.js"></script>
    END
    if($NEXT eq "cpu" && $vic == 0 && $draw == 0) {
        print <<"        END";
            <meta http-equiv="refresh"
             content="0;url=$ENV{'SCRIPT_NAME'}?data=$DATA&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}">
        END
    }

=pod
$ban->[11][4] = 1;
my $count = 1;
for my $ban (@$ban) {
print "<br>\n";
  for my $column (@$ban) {
    print "$column\n";
  }
}
=cut

#===============================#盤を表示

#for my $ban (@$ban) {
#print "<br>\n";
# for my $column (@$ban) {
#   print "$column\n";
# }
#}


    print <<"    END";
        <title>重力付き四目並べ -対局中-</title>
        <style type="text/css">
        <!--
            table    { margin-bottom:10px; width:580px; background:#ec8; border:1px solid #333 }
            th    { padding:3px; background:#99f }
            td    { width:50px; height:50px; font-size:30px; text-align:center; border:1px solid #333 }
            td a    { width:100%; height:100%; display:block }
            a    { text-decoration:none }
            .msg    { padding:3px; color: #000; font-size:25px; font-weight:bold; text-align:center }
            a:hover { text-decoration:underline;}
        //-->
        </style>
        </head>
        <body>

        <center>
        <font size="6"><b>重力付き四目並べ</b></font>
        <hr>
        <b>$MSG2</b>
    END

    if($vic == 1){
        print qq(<font size="5"><b><a href="$ENV{'SCRIPT_NAME'}?data=&player_turn=$FORM{'player_turn'}&next_cpu=-1">再スタート</a> <a href="./index.cgi">TOP</a></b></font><br>);
    if($FORM{'next_cpu'} == 2){
    print qq(<font size="5" color="#f00"><b>$MSG</b></font>);
    }elsif($FORM{'next_cpu'} == 1){
    print qq(<font size="5" color="#00f"><b>$MSG</b></font>);
  }
  }elsif($draw == 1){
    print qq(<font size="5"><b><a href="$ENV{'SCRIPT_NAME'}?data=&player_turn=$FORM{'player_turn'}&next_cpu=-1">再スタート</a> <a href="./index.cgi">TOP</a></b></font><br>);
    print qq(<font size="5" color="#32CD32"><b>$MSG</b></font>);
  }elsif($FORM{'next_cpu'} == 2){ #CPU
        print qq(<font size="5"><br></font>);
        print qq(<font size="5"><b>$MSG</b><img src="../image/loading.gif"></font>);
  }else{
        print qq(<font size="5"><br></font>);
        print qq(<font size="5"><b>$MSG</b></font>);
      }

    print <<"    END";
        </center>
        <table cellspacing="0" align="center">
        <tr>
        <th colspan="4" align="left"></th>
        <th colspan="4" align="right">
            コンピュータ $CPU
    END
if($FORM{'player_turn'} eq "1") {
print qq((後手)); #後手
  }else{
print qq((先手)); #先手
  }
print <<"    END";
        </th>
        </tr>
        </table>
    END

    if($vic == 0){
    print qq(<table cellspacing="0" cellpadding="0" align="center" border=1 class="cellcolor:#edae2f">);
}elsif($vic == 1){
    print qq(<table cellspacing="0" cellpadding="0" align="center" border=1>);
}

#===============================#盤面作成
my $count = 1;
my $str_j;
my $te_last;
my $te_last_check=0;

$te_last = @list[0];

if($te_last eq "a"){
 $te_last = 10;
}elsif($te_last eq "b"){
 $te_last = 11;
}

    for($i = 0; $i < 12; $i++) {
    	if($i != 0) {
    		print qq(<tr>\n);
    	}
    	    for($j = 0; $j < 12; $j++) {
    	    	           	if($j == 10){
           		$str_j = "a";
           		}elsif($j == 11){
           			$str_j = "b";
           			}else{
           				$str_j = $j . "";
           			}
    	    	          my $DATA2 = $DATA . $str_j."\n";
           # print qq(<td> </td>\n);
#===============================#セルにマウスを置いた時に、プレイヤーが置ける場所を表示
           if($i == 11 && $ban->[$i][$j] == 0){
           	if($FORM{'player_turn' || $vic == 1 || $draw == 1} == 1){
           		if($NEXT eq "cpu") {
             print qq(<td><img src="../image/invisible.png"  id="col$j"></td>\n);
           			}else{
             print qq(<td><a href="$ENV{'SCRIPT_NAME'}?data=$DATA2&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}" onmouseover="document.getElementById('col$j').src='../image/black2.png'" onmouseout="document.getElementById('col$j').src='../image/invisible.png'"><img src="../image/invisible.png"  id="col$j"></a></td>\n);
         }
    }else{
    	if($NEXT eq "cpu" || $vic == 1 || $draw == 1) {
             print qq(<td><img src="../image/invisible.png"  id="col$j"></td>\n);
    		}else{
             print qq(<td><a href="$ENV{'SCRIPT_NAME'}?data=$DATA2&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}" onmouseover="document.getElementById('col$j').src='../image/white2.png'" onmouseout="document.getElementById('col$j').src='../image/invisible.png'"><img src="../image/invisible.png"  id="col$j"></a></td>\n);
    		}
    }
           }
           elsif($i < 11 && ($ban->[$i][$j] == 0 && $ban->[$i + 1][$j] != 0)){
           	if($FORM{'player_turn'} == 1){
           		    	if($NEXT eq "cpu" || $vic == 1 || $draw == 1) {
             print qq(<td><img src="../image/invisible.png"  id="col$j"></td>\n);
           		    		}else{
             print qq(<td><a href="$ENV{'SCRIPT_NAME'}?data=$DATA2&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}" onmouseover="document.getElementById('col$j').src='../image/black2.png'" onmouseout="document.getElementById('col$j').src='../image/invisible.png'"><img src="../image/invisible.png"  id="col$j"></a></td>\n);
         }
    }else{
    	           	if($NEXT eq "cpu" || $vic == 1 || $draw == 1) {
             print qq(<td><img src="../image/invisible.png"  id="col$j"></td>\n);
    	           		}else{
             print qq(<td><a href="$ENV{'SCRIPT_NAME'}?data=$DATA2&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}" onmouseover="document.getElementById('col$j').src='../image/white2.png'" onmouseout="document.getElementById('col$j').src='../image/invisible.png'"><img src="../image/invisible.png"  id="col$j"></a></td>\n);
         }
    }
           }
#===============================#
           elsif($ban->[$i][$j] == 0){
          if($FORM{'player_turn'} == 1){
          	    	           	if($NEXT eq "cpu" || $vic == 1 || $draw == 1) {
             print qq(<td><img src="../image/invisible.png"></td>\n);
          	    	           		}else{
             print qq(<td><a href="$ENV{'SCRIPT_NAME'}?data=$DATA2&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}" onmouseover="document.getElementById('col$j').src='../image/black2.png'" onmouseout="document.getElementById('col$j').src='../image/invisible.png'"><img src="../image/invisible.png"></a></td>\n);
         }
             }else{
             	if($NEXT eq "cpu" || $vic == 1 || $draw == 1) {
             print qq(<td><img src="../image/invisible.png"></td>\n);
             	}else{
             print qq(<td><a href="$ENV{'SCRIPT_NAME'}?data=$DATA2&player_turn=$FORM{'player_turn'}&next_cpu=$FORM{'next_cpu'}" onmouseover="document.getElementById('col$j').src='../image/white2.png'" onmouseout="document.getElementById('col$j').src='../image/invisible.png'"><img src="../image/invisible.png"></a></td>\n);
         }
             }
           }else{
           	if($ban->[$i][$j] == 1){
              if($te_last == $j && $te_last_check == 0 && $FORM{'next_cpu'} == 1 && $vic == 0){
             print qq(<td bgcolor="#b39966"><img src="../image/black.png"></td>\n);
             $te_last_check = 1;
              }else{
           	 print qq(<td><img src="../image/black.png"></td>\n);
            }
           	}elsif($ban->[$i][$j] % 2 == 1){
           	print qq(<td bgcolor="#ff99aa"><img src="../image/black.png"></td>\n);
           	}elsif($ban->[$i][$j] == 2){
              if($te_last == $j && $te_last_check == 0 && $FORM{'next_cpu'} == 1 && $vic == 0){
             print qq(<td bgcolor="#b39966"><img src="../image/white.png"></td>\n);
             $te_last_check = 1;
              }else{
             print qq(<td><img src="../image/white.png"></td>\n);
           }
           	}elsif($ban->[$i][$j] % 2 == 0){
             print qq(<td bgcolor="#ff99aa"><img src="../image/white.png"></td>\n);
           	}
           	$count++;
           }
        if($j == 11) {
            print qq(</tr>\n);
        }
    }
}

    print <<"    END";
        </table>
        <table cellspacing="0" align="center">
        <tr>
        <th colspan="4" align="left">$PLAYER プレイヤー
    END
if($FORM{'player_turn'} eq "1") {
print qq((先手)); #先手
  }else{
print qq((後手)); #後手
  }
 print <<"    END";
        </th>
        <th colspan="4" align="right">
        </th>
        </tr>
        </table>
        <center>
    END
    if(length($DATA) > 0){
print length($DATA);
print qq( 手)
}
        print qq(</center></body></html>)
}

#====================================================================フォームデータ取り込み
sub    loadForm
{
=pod
	print qq(Content-type: text/html; charset=Shift_JIS\n\n);
    binmode STDIN, ':encoding(cp932)';
    binmode STDOUT, ':encoding(cp932)';
    binmode STDERR, ':encoding(cp932)';
=cut

    my    ($query, $pair);
    if($ENV{'REQUEST_METHOD'} eq 'POST') {
        read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
    }
    else {
        $query = $ENV{'QUERY_STRING'};
    }
    foreach $pair (split(/&/, $query)) {
        my    ($key, $value) = split(/=/, $pair);
        $value =~ tr/+/ /;
        $value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
        $FORM{$key} = $value;
    }
}

#====================================================================エラー処理
sub error {
my ($error) = @_;
    print qq(Content-type: text/html; charset=UTF-8\n\n);
         print <<"        END";
            <meta http-equiv="refresh"
             content="0;url=error.cgi?error=$error">
        END
        exit(0);
}

#====================================================================成績を記録する
sub data_result {
my $file = "data_result.txt";
my ($check) = @_;
local $SIG{ALRM} = sub { die "timeout" };
alarm 10;#アラームを10秒に設定
#ログ読み込み&ロック
open(FILEHANDLE,"+<$file"); #読み書きモードでファイルオープン
flock(FILEHANDLE, 2);  #ロック確認 ロック
my @data = <FILEHANDLE>; #@dataに読み込み
alarm 0;

alarm 0;#アラーム解除
if($@) {&error;}; # タイムアウト時の処理 別にsub errorが必要になる

#〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
if($check == 1){
@data[0] = @data[0]+1 . "\n";
}elsif($check == 2){
@data[1] = @data[1]+1 . "\n";
}elsif($check == 3){
@data[2] = @data[2]+1 . "\n";
}
#〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜

seek(FILEHANDLE, 0, 0);  # ファイルポインタを先頭にセット
print FILEHANDLE @data;  # ファイルに書き込む
truncate(FILEHANDLE, tell(FILEHANDLE));  # ファイルサイズを書き込んだサイズにする
close (FILEHANDLE);  #closeで自動にロック解除
};


#====================================================================棋譜を記録する
sub data_kifu {
my $file = "data_kifu.txt";
my ($check) = @_;
local $SIG{ALRM} = sub { die "timeout" };
alarm 10;#アラームを10秒に設定
#ログ読み込み&ロック
open(FILEHANDLE,">>$file"); #読み書きモードでファイルオープン
flock(FILEHANDLE, 2);  #ロック確認 ロック
my @data = <FILEHANDLE>; #@dataに読み込み
alarm 0;

alarm 0;#アラーム解除
if($@) {&error;}; # タイムアウト時の処理 別にsub errorが必要になる

#〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
if($check == 1){
@data[0] = $DATA . "\n";
}
#〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜

seek(FILEHANDLE, 0, 0);  # ファイルポインタを先頭にセット
print FILEHANDLE @data;  # ファイルに書き込む
truncate(FILEHANDLE, tell(FILEHANDLE));  # ファイルサイズを書き込んだサイズにする
close (FILEHANDLE);  #closeで自動にロック解除
};
