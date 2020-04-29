function match(param){
    var timetable = param;
    var array = ["monday", "tuesday", "wednesday", "thursday", "friday"];
    var color = ["green", "turquoise", "navy", "blue", "purple", "gray", "orange", "yellow"];
    var coloridx = 0;
    for(i = 0;i<5;i++){
        var object = document.getElementsByClassName(array[i]);
        console.log(object);
        for(j = 0;j<timetable[i].length;j++){
            console.log(timetable[i][j]);
            var curstarthour = parseInt(timetable[i][j][0][0])*10+parseInt(timetable[i][j][0][1]);
            var curstartmin = parseInt(timetable[i][j][0][3])*10+parseInt(timetable[i][j][0][4]);
            var curendhour = parseInt(timetable[i][j][1][0])*10+parseInt(timetable[i][j][1][1]);
            var curendmin = parseInt(timetable[i][j][1][3])*10+parseInt(timetable[i][j][1][4]);
            console.log(curstarthour*100+curstartmin);
            console.log(curendhour*100+curendmin);
            var prevendhour;
            var prevendmin;
            if(j==0){
                prevendhour = 9;
                prevendmin = 0;
            }
            else{
                prevendhour = parseInt(timetable[i][j-1][1][0])*10+parseInt(timetable[i][j-1][1][1]);
                prevendmin  = parseInt(timetable[i][j-1][1][3])*10+parseInt(timetable[i][j-1][1][4]);
            }
            var hourdif = (curstarthour-prevendhour)*60;
                var mindif = curstartmin-prevendmin;
                var difval = hourdif+mindif;
                console.log(difval);
                var curclass = document.createElement('div');
                curclass.className += ("class "+color[coloridx]);
                coloridx = (coloridx+1)%color.length;
                curclass.style.marginTop = difval/10+"vh";
                curclass.innerHTML = timetable[i][j][2];
                curclass.setAttribute('data-tooltip', timetable[i][j][3]);
                object[0].appendChild(curclass);
        }
    }
}