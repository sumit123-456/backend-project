
// =================== BAR DATA ===================
const deptDatasets = {
  "all": { labels:["Eng","HR","Sales","Ops","Fin","Legal"], data:[85,60,92,74,68,50] },
  "engineering": { labels:["Backend","Frontend","QA"], data:[40,30,15] },
  "hr": { labels:["Recruit","Benefits"], data:[20,18] },
  "sales": { labels:["North","South","East","West"], data:[23,27,21,21] }
};

// =================== PIE DATA ===================
const pieDataBase = {
  labels: ["Present", "Absent", "Late", "Remote"],
  data: [60, 20, 10, 10]
};

// =================== DEPARTMENT BAR CHART ===================
const bar = new Chart(document.getElementById("barChart"), {
  type: "bar",
  data: {
    labels: deptDatasets["all"].labels,
    datasets: [{
      data: deptDatasets["all"].data,
      backgroundColor: ["#0B5C63", "#0B7368", "#0FA088", "#2BA68B", "#F2B33D", "#D64550"],
      borderRadius: 10,
      barThickness: 30
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } }
  }
});

// Filter change
document.getElementById("deptFilter").onchange = function(){
  let ds = deptDatasets[this.value];
  bar.data.labels = ds.labels;
  bar.data.datasets[0].data = ds.data;
  bar.update();
};

document.getElementById("yearFilter").onchange = function(){
  let scale = this.value === "2025" ? 1 : this.value === "2024" ? 0.92 : 0.85;
  bar.data.datasets[0].data = deptDatasets["all"].data.map(n => Math.round(n * scale));
  bar.update();
};

// =================== ATTENDANCE PIE CHART ===================
const pieChart = new Chart(document.getElementById("pieChart"), {
  type: "doughnut",
  data: {
    labels: pieDataBase.labels,
    datasets: [{
      data: pieDataBase.data,
      backgroundColor: ["#0b7368", "#d64550", "#f2b33d", "#2ba68b"],
      hoverOffset: 10
    }]
  },
  options: { responsive: true, maintainAspectRatio: false }
});

// Month filter
document.getElementById("pieMonthFilter").onchange = function(){
  let c = ["#0b7368","#d64550","#f2b33d","#2ba68b"];
  if(this.value==="feb") c=["#19647e","#ff4d6d","#ffbd39","#68b684"];
  if(this.value==="mar") c=["#013c5a","#d64550","#f2b33d","#55a6a6"];

  pieChart.data.datasets[0].backgroundColor = c;
  pieChart.update();
};
