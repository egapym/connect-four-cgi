#!/usr/bin/perl --

use utf8;
use open ":utf8";

my $file = "data_result.txt";

open(FILEHANDLE,"$file"); #読み書きモードでファイルオープン
@data = <FILEHANDLE>; #@dataに読み込み
close (FILEHANDLE);  #closeで自動にロック解除

if(@data[0] + @data[1] != 0){
$data_sum = @data[0] + @data[1] + @data[2];
$wp_player = @data[0] / ($data_sum - @data[2]) * 100;
$wp_player = sprintf("%.1f",$wp_player);
$wp_cpu = @data[1] / ($data_sum - @data[2]) * 100;
$wp_cpu = sprintf("%.1f",$wp_cpu);
}else{
$wp_player = 0;
$wp_player = sprintf("%.1f",$wp_player);
$wp_cpu = 0;
$wp_cpu = sprintf("%.1f",$wp_cpu);
}
printData();        #HTML出力

exit(0);

#====================================================================HTML出力
sub    printData
{
 print qq(Content-type: text/html; charset=UTF-8\n\n);
 print <<"    END";
    <html>
    <head>
    <title>重力付き四目並べ</title>
    <style type="text/css">
    <!--
    a       { text-decoration:none;}
    a:hover { text-decoration:underline;}
    -->
    </style>
    </head>

    <body>
    <center>
    <font size="6"><b>重力付き四目並べ</b></font>
    <hr>
    プレイヤーの手番を選択して対局開始！
    <table>
    <tr align="center">
    <td width="150"><a href="game.cgi?data=&player_turn=1&next_cpu=-1"><font size="7">先手</font></a></td>
    <td width="150"><a href="game.cgi?data=&player_turn=2&next_cpu=-1"><font size="7">後手</font></a></td>
    </tr>
    </table>
    <br>
    <b><font size="4">- ルール -</font></b><br>
    交互にコマを盤の下から積み重ねていき、<br>
    先に縦・横・斜めいずれかに直線状に4つ、または4つ以上並べた方の勝利です。<br><br><br>
    <b><font size="4">- すべての対戦結果 -</font></a><br></b>
対局回数: <b>$data_sum</b><br>
プレイヤー勝利: <b>@data[0]($wp_player%)</b>　
コンピュータ勝利: <b>@data[1]($wp_cpu%)</b>　
引き分け: <b>@data[2]</b>
    </center>
    </body>
    </html>
    END
}