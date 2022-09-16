// 사이드바 open을 위한 함수
function openNav() {
    // if(document.getElementById("gubun").value != '전체조회'){
    //     alert("차트 기능은 전체조회일때만 가능합니다");
    //     return
    // }
    document.getElementById("mySidenav").style.width = "250px";
}
// 사이드바 close를 위한 함수
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
// 비동기 테이블 출력을 위한 ajax함수
function checkDb(){
    if(!document.getElementById("datemin").value || !document.getElementById("datemax").value){
        hideSpinner();
        alert("시작날짜와 종료날짜 모두 입력해주세요");
        return
    }
    showSpinner();
    document.getElementById("tables").style='display:block';
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            data = this.responseText;  
            data = JSON.parse(data);
            temp = 0;
            let dateminTemp = new Date(document.getElementById("datemin").value);
            let datemaxTemp = new Date(document.getElementById("datemax").value);
            const diffDate = datemaxTemp.getTime() - dateminTemp.getTime();
            const dat = diffDate/(1000*60*60*24)+1;
            
            console.log(dat);
            if(data.test == "없음"){
                hideSpinner();
                alert("해당 데이터가 없습니다");
                return
            }
            var tableData = `<tr>`;
            for(var i in data){
                tableData = tableData +`<td>`+data[i].create_dt
                            +`</td><td>`+Number(data[i].conf_case).toLocaleString()
                            +`</td><td>`+data[i].conf_caserate 
                            +`</td><td>`+data[i].critical_rate
                            +`</td><td>`+data[i].death.toLocaleString()
                            +`</td><td>`+data[i].death_rate
                            +`</td><td>`+data[i].gubun
                            +`</td></tr>`;
                if(data[i].gubun=='남성'||data[i].gubun=='여성'){
                    temp = (temp+Number(data[i].conf_case))/dat;
                }
            }
            hideSpinner();
            document.getElementById("info").innerHTML = tableData;
            document.getElementById("total").innerHTML = temp.toLocaleString();
            
        }
    };
    xhttp.open("POST", "infodate");   
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    queryString = "datemin="+document.getElementById("datemin").value
                    +"&datemax="+document.getElementById("datemax").value
                    +"&gubun="+getGubunValue();
    xhttp.send(queryString);
}
// 비동기 차트 출력을 위한 ajax함수
function drawChart(chart){
    showSpinner();
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            url = this.responseText;  
            url = JSON.parse(url);
            if(url.test == "없음"){
                hideSpinner();
                alert("해당 데이터가 없습니다");
                return
            }
            console.log(url.url);
            hideSpinner();
            document.getElementById("imagesBox").style.display = 'block';
            document.getElementById("images").src = url.url;
            // document.getElementById("info").innerHTML = tableData;
        }
    };
    xhttp.open("POST", "chart");   
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    queryString = "datemin="+document.getElementById("datemin").value
                  +"&datemax="+document.getElementById("datemax").value 
                  +"&chart="+chart;
    xhttp.send(queryString);
}

// checkbox 다중 배열 값을 받기 위해
function getGubunValue(){
    const query = 'input[name="gubun"]:checked';
    const selectedEls = document.querySelectorAll(query)
    let result = [];
    selectedEls.forEach((el) =>{
        result.push(el.value);
    });
    return result;
}

function getOptionValue(){
    const query = 'input[name="option"]:checked';
    const selectedEls = document.querySelectorAll(query)
    let result = [];
    selectedEls.forEach((el) =>{
        result.push(el.value);
    });
    return result;
}

function mainCont(){
    showSpinner();
    const temp = getOptionValue();
    if(temp.includes("Chart")&&temp.includes("Table")){
        showChart();
        checkDb();
       
    }else if(temp.includes("Chart")&&!temp.includes("Table")){
        document.getElementById("tables").style.display='none';
        hideSpinner();
        showChart();
        
        
    }else if(!temp.includes("Chart")&&temp.includes("Table")){
        document.getElementById('Chart').style.display='none';
        checkDb();
        
    }else if(!temp.includes("Chart")&&!temp.includes("Table")){
        hideSpinner();
        alert("옵션에서 한가지 이상을 선택해주세요");
    }
    
}

function showSpinner() {
    console.log("showSpinner")
    document.getElementsByClassName('layerPopup')[0].style.display='block';
}
function hideSpinner() {
    console.log("hideSpinner")
    document.getElementsByClassName('layerPopup')[0].style.display='none';
}
function showChart(){
    document.getElementById('Chart').style.display='block';
}


function openTab(evt, graphType) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(graphType).style.display = "block";
    evt.currentTarget.className += " active";
  }
  document.getElementById("defaultOpen").click();