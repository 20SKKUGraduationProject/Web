HashMap = function(){
    this.map = new Array();
};

HashMap.prototype = {
    put: function(key, value){
        this.map[key] = value;
    },
    get: function(key){
        return this.map[key];
    },
}

function match(param){
    var timetable = param;
    var array = ["monday", "tuesday", "wednesday", "thursday", "friday"];
    var color = ["green", "turquoise", "navy", "blue", "purple", "gray", "orange", "yellow"];
    var coloridx = 0;
    var courselist = new HashMap();
    for(i = 0;i<5;i++){
        var object = document.getElementsByClassName(array[i]);
        for(j = 0;j<timetable[i].length;j++){
            var curstarthour = parseInt(timetable[i][j][0][0])*10+parseInt(timetable[i][j][0][1]);
            var curstartmin = parseInt(timetable[i][j][0][3])*10+parseInt(timetable[i][j][0][4]);
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
            var curclass = document.createElement('div');
            var duptest = courselist.get(timetable[i][j][2]);
            if(duptest==null){
                courselist.put(timetable[i][j][2], color[coloridx]);
                curclass.className += ("class "+color[coloridx]);
                coloridx = (coloridx+1)%color.length;
            }
            else{
                curclass.className += ("class "+duptest);
            }
            curclass.style.marginTop = difval/10+"vh";
            curclass.innerHTML = timetable[i][j][2];
            curclass.setAttribute('data-tooltip', timetable[i][j][3]);
            object[0].appendChild(curclass);
        }
    }
}