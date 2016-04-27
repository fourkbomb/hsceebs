data = require('./data.json');
subjects = require('./subjects.json');
subjects.sort();
fixed = {}

function parse_time(time) {
    var sTime = time.split(".");
    console.log(time,sTime);
    var isPm;
    if (sTime.length > 1)
        isPm = sTime[1].substr(-2) == "pm";
    else
        isPm = sTime[0].substr(-2) == "pm";
    var sHour = Number(sTime[0]) + (isPm ? 12 : 00);
    var sMin;
    if (sTime.length > 1)
        sMin = Number(sTime[1].split(isPm ? "p" : "a")[0]);
    else
        sMin = 0;
    return [sHour,sMin];
}

Date.prototype.addHours = function(hours, minutes) {
    return this.setHours(this.getHours() + hours, this.getMinutes() + minutes);
}

for (var key in data) {
    console.log(key);
    if (!data.hasOwnProperty(key)) continue;
    var col = data[key];
    for (var date in col) {
        console.log(date);
        if (!col.hasOwnProperty(date) || date == ' ') continue;
        var sdate = new Date(date); 
        if (sdate.valueOf() == NaN)  {
            console.write("invalid date:",date);
            continue;
        }
        var papers = col[date];
        for (var i in papers) {
            console.log(i);
            var sTime = parse_time(papers[i].times[0]);
            var eTime = parse_time(papers[i].times[1]);
            var sDate = new Date(sdate);
            sDate.addHours(sTime[0], sTime[1]);
            var eDate = new Date(sdate);
            eDate.addHours(eTime[0], eTime[1]);
            var newData = papers[i];
            newData.times[0] = sDate.valueOf();
            newData.times[1] = eDate.valueOf();
            var idx = subjects.indexOf(papers[i].name);
            if (!(idx in fixed)) {
                fixed[idx] = [newData];
            } else {
                fixed[idx].push(newData);
            }
        }
    }
}

console.log(JSON.stringify(fixed));


