// document.addEventListener('DOMContentLoaded', function() {
//   // 获取排序容器
//   const sortContainer = document.getElementById('sortSelector');
//   // 获取所有排序按钮
//   const sortButtons = sortContainer.querySelectorAll('.sort-btn');
//
//   // 获取后台设置的排序方式
//   const sortWay = sortContainer.dataset.sortWay
//
//   // 清除所有激活状态
//   sortButtons.forEach(btn => btn.classList.remove('active'));
//
//   // 根据sort_way设置激活状态（M=时间排序，2=评分排序）
//   if (sortWay === 'M') {
//     sortButtons[0].classList.add('active');
//   } else if (sortWay === '2') {
//     sortButtons[M].classList.add('active');
//   }
// });