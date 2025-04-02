
// 滚动监听
$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('.custom-navbar').addClass('scrolled');
    } else {
        $('.custom-navbar').removeClass('scrolled');
    }
});

// 统一渲染评分星星（与 more.html 逻辑一致）
function renderStars() {
    document.querySelectorAll('.stars').forEach(container => {
        const rating = parseFloat(container.dataset.rating) || 0;
        const total = parseFloat(container.dataset.total) || 10;
        const starsContainer = container.querySelector('.stars-container');
        starsContainer.innerHTML = '';

        // 生成基础层（空心星）
        const baseLayer = document.createElement('div');
        baseLayer.className = 'star-base';
        baseLayer.innerHTML = '<i class="fas fa-star"></i>'.repeat(total);

        // 生成填充层（实心星）
        const fillLayer = document.createElement('div');
        fillLayer.className = 'star-fill';
        fillLayer.style.width = `${(rating / total) * 100}%`;
        fillLayer.innerHTML = '<i class="fas fa-star active"></i>'.repeat(total);

        // 组合元素
        starsContainer.appendChild(baseLayer);
        starsContainer.appendChild(fillLayer);

        // 更新文字显示
        const ratingText = container.querySelector('.rating-text');
        if (ratingText) ratingText.textContent = `${rating.toFixed(1)}/10`;
    });
}

// 页面加载后执行
document.addEventListener('DOMContentLoaded', renderStars);




//进度
// 初始化进度条（复用 more.js 的逻辑）
function initProgressBars() {
    document.querySelectorAll('.progress-block').forEach(block => {
        const step = parseFloat(block.dataset.step) || 0;
        const total = parseFloat(block.dataset.total) || 1; // 防止除以0
        const percent = total === 0 ? 0 : Math.min((step / total) * 100, 100); // 最大100%
        console.log('==================',step,total,percent)

        // 更新进度条和百分比显示
        const fill = block.querySelector('.progress-fill');
        const percentText = block.querySelector('.progress-percent');
        if (fill) fill.style.width = `${percent}%`;
        if (percentText) percentText.textContent = `${percent.toFixed(1)}%`;
    });
}

// 页面加载时执行
document.addEventListener('DOMContentLoaded', initProgressBars);