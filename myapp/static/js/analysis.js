let chart = null;


// 初始化图表
function initChart() {
    const chartDom = document.getElementById('tagChart');
    if (!chartDom) {
        console.error('找不到图表容器 #tagChart');
        return;
    }
    chart = echarts.init(chartDom);
    console.log('图表初始化完成');
}

// 从API加载数据并更新图表
function loadChartData() {
    console.log('开始请求数据...');
    fetch('/api/get_tag_stats/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('接收到数据:', data);
            if (data.chart_data) {
                const option = {
                    tooltip: {trigger: 'item'},
                    series: [{
                        type: 'pie',
                        radius: '70%',
                        data: data.chart_data,
                        emphasis: {itemStyle: {shadowBlur: 10}},
                        label: {formatter: '{b}: {d}%'}
                    }]
                };
                chart.setOption(option);
                console.log('图表更新成功');
            } else {
                console.error('数据格式错误:', data);
            }
        })
        .catch(error => {
            console.error('请求失败:', error);
            alert('无法加载图表数据，请检查控制台');
        });
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM加载完成');
    initChart();
    loadChartData();  // 首次自动加载
    // 绑定按钮点击事件
    document.getElementById('refreshChart')?.addEventListener('click', loadChartData);
});

// 窗口变化时自适应
window.addEventListener('resize', () => {
    if (chart) {
        chart.resize();
        console.log('图表已自适应窗口');
    }
});




// 新增趋势图相关代码
let trendChart = null;

function initTrendChart() {
    const chartDom = document.getElementById('trendChart');
    trendChart = echarts.init(chartDom);
}

function loadTrendData() {
    fetch('/api/get_trend_stats/')
        .then(response => response.json())
        .then(data => {
            const option = {
                tooltip: { trigger: 'axis' },
                xAxis: {
                    type: 'category',
                    data: data.labels,
                    axisLabel: { rotate: 45 }
                },
                yAxis: { type: 'value' },
                series: [{
                    type: 'bar',
                    data: data.values,
                    itemStyle: {
                        color: '#7154a8' // 使用与文字相同的紫色
                    }
                }]
            };
            trendChart.setOption(option);
        });
}

// 修改DOMContentLoaded事件
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    initTrendChart();  // 新增初始化
    loadChartData();
    loadTrendData();  // 新增数据加载
    // 新增窗口resize处理
    window.addEventListener('resize', () => {
        trendChart?.resize();
    });
});