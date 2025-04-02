

document.addEventListener('DOMContentLoaded', function() {
    let selectedTags = [];
    const maxTags = 3;
    let searchTimeout = null;

    // 标签点击处理
    document.querySelectorAll('.tag-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const tagId = btn.dataset.tagId;
            const isActive = btn.classList.contains('active');

            if (isActive) {
                selectedTags = selectedTags.filter(id => id !== tagId);
                btn.classList.remove('active');
            } else {
                if (selectedTags.length >= maxTags) {
                    const removedId = selectedTags.shift();
                    document.querySelector(`.tag-item[data-tag-id="${removedId}"]`).classList.remove('active');
                }
                selectedTags.push(tagId);
                btn.classList.add('active');
            }
            updateSelectedTags();
        });
    });

    // 更新已选标签显示
    // filter.js 修改 updateSelectedTags 函数
function updateSelectedTags() {
    const container = document.getElementById('selectedTagsContainer');
    // 新增计数器HTML
    const counterHtml = `
        <div class="selected-counter me-2">
            已选择 ${selectedTags.length}/${maxTags}
        </div>
    `;

    container.innerHTML = counterHtml + selectedTags.map(tagId => {
        const tag = document.querySelector(`.tag-item[data-tag-id="${tagId}"]`);
        return `
            <span class="badge bg-success me-1">
                ${tag.textContent.trim()}
                <button type="button" class="btn-close btn-close-white ms-1" 
                        data-tag-id="${tagId}"></button>
            </span>
        `;
    }).join('');
}

    // 移除标签
    document.getElementById('selectedTagsContainer').addEventListener('click', e => {
        if (e.target.classList.contains('btn-close')) {
            const tagId = e.target.dataset.tagId;
            selectedTags = selectedTags.filter(id => id !== tagId);
            document.querySelector(`.tag-item[data-tag-id="${tagId}"]`).classList.remove('active');
            updateSelectedTags();
        }
    });

    // 标签搜索功能
    const searchInput = document.getElementById('tagSearchInput');
    const suggestionsBox = document.getElementById('searchSuggestions');
    const noMatchAlert = document.getElementById('noMatchAlert');

    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = this.value.trim().toLowerCase();

            if (query.length > 0) {
                fetch(`/api/search_tags?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.results.length > 0) {
                            suggestionsBox.innerHTML = data.results.map(tag => `
                                <div class="search-suggestion-item list-group-item list-group-item-action"
                                     data-tag-id="${tag.id}">
                                    ${tag.name}
                                </div>
                            `).join('');
                            suggestionsBox.classList.remove('d-none');
                            noMatchAlert.classList.add('d-none');
                        } else {
                            suggestionsBox.classList.add('d-none');
                            noMatchAlert.classList.remove('d-none');
                        }
                    });
            } else {
                suggestionsBox.classList.add('d-none');
                noMatchAlert.classList.add('d-none');
            }
        }, 300);
    });

    // 搜索建议点击
    // filter.js 修改建议点击事件
suggestionsBox.addEventListener('click', e => {
    const item = e.target.closest('.search-suggestion-item');
    if (item) {
        const tagId = item.dataset.tagId;
        const tagName = item.textContent.trim();
        const tagCloud = document.querySelector('.tag-cloud');

        // 检查标签是否已存在
        let tagBtn = document.querySelector(`.tag-item[data-tag-id="${tagId}"]`);
        if (!tagBtn) {
            // 动态创建新标签按钮
            tagBtn = document.createElement('button');
            tagBtn.className = 'tag-item btn btn-outline-primary btn-sm';
            tagBtn.dataset.tagId = tagId;
            tagBtn.textContent = tagName;

            // 绑定点击事件（与原生标签相同逻辑）
            tagBtn.addEventListener('click', function() {
                const isActive = this.classList.contains('active');
                const tagId = this.dataset.tagId;

                if (isActive) {
                    selectedTags = selectedTags.filter(id => id !== tagId);
                    this.classList.remove('active');
                } else {
                    if (selectedTags.length >= maxTags) {
                        const removedId = selectedTags.shift();
                        document.querySelector(`.tag-item[data-tag-id="${removedId}"]`).classList.remove('active');
                    }
                    selectedTags.push(tagId);
                    this.classList.add('active');
                }
                updateSelectedTags();
            });

            tagCloud.prepend(tagBtn); // 将新标签插入到标签云最前面
        }

        // 触发选中状态
        if (!selectedTags.includes(tagId)) {
            if (selectedTags.length >= maxTags) {
                const removedId = selectedTags.shift();
                document.querySelector(`.tag-item[data-tag-id="${removedId}"]`).classList.remove('active');
            }
            selectedTags.push(tagId);
            tagBtn.classList.add('active');
            updateSelectedTags();
        }

        searchInput.value = '';
        suggestionsBox.classList.add('d-none');
    }
});
});





document.addEventListener('DOMContentLoaded', function() {

    const currentMonth = new Date().toISOString().slice(0, 7);
    const allTimeCheck = document.getElementById('allTimeCheck');
    const timeRangePicker = document.getElementById('timeRangePicker');
    const timeDisplay = document.querySelector('.time-display');

    // 初始化时间输入最大值
    document.querySelectorAll('input[type="month"]').forEach(input => {
        input.max = currentMonth;
    });

    // 全部时间复选框逻辑
    allTimeCheck.addEventListener('change', function() {
        timeRangePicker.style.display = this.checked ? 'none' : 'block';
        updateTimeDisplay();
    });

    // 时间输入变化监听
    document.querySelectorAll('input[type="month"]').forEach(input => {
        input.addEventListener('change', function() {
            const start = document.querySelector('.start-month').value;
            const end = document.querySelector('.end-month').value;

            // 验证时间范围
            if (start && end && start > end) {
                alert('结束时间不能早于开始时间');
                this.value = start; // 自动修正为开始时间
                return;
            }

            // 动态调整最小值
            if (this.classList.contains('start-month')) {
                document.querySelector('.end-month').min = start;
            }

            updateTimeDisplay();
        });
    });

    function updateTimeDisplay() {
        if (allTimeCheck.checked) {
            timeDisplay.textContent = '时间范围：全部';
            return;
        }

        const start = document.querySelector('.start-month').value || '未选择';
        const end = document.querySelector('.end-month').value || '未选择';
        timeDisplay.textContent = `时间范围：${start} 至 ${end}`;
    }
});




//评分选择

document.addEventListener('DOMContentLoaded', function() {


    // 评分组件初始化
    const ratingElements = {
        allCheck: document.getElementById('allRatingCheck'),
        rangePicker: document.getElementById('ratingRangePicker'),
        display: document.querySelector('.rating-display'),
        min: document.getElementById('minRating'),
        max: document.getElementById('maxRating')
    };

    // 全部评分切换
    ratingElements.allCheck.addEventListener('change', function() {
        ratingElements.rangePicker.style.display = this.checked ? 'none' : 'block';
        updateRatingDisplay();
    });

    // 按钮事件绑定
    document.querySelectorAll('#minMinus, #minPlus').forEach(btn => {
        btn.addEventListener('click', () => adjustRating('min', btn.id.includes('Plus')));
    });
    document.querySelectorAll('#maxMinus, #maxPlus').forEach(btn => {
        btn.addEventListener('click', () => adjustRating('max', btn.id.includes('Plus')));
    });

    // 输入框事件
    [ratingElements.min, ratingElements.max].forEach(input => {
        input.addEventListener('input', () => validateRatingRange());
    });

    // 数值调整函数
    function adjustRating(type, isIncrease) {
        const input = ratingElements[type];
        let value = parseFloat(input.value) || 0;
        value = isIncrease ? value + 0.5 : value - 0.5;
        input.value = Math.min(10, Math.max(0, value)).toFixed(1);
        validateRatingRange();
    }

    // 范围验证
    function validateRatingRange() {
        let min = parseFloat(ratingElements.min.value) || 0;
        let max = parseFloat(ratingElements.max.value) || 10;

        // 自动修正范围
        if (min > max) {
            [min, max] = [max, min];
            ratingElements.min.value = min.toFixed(1);
            ratingElements.max.value = max.toFixed(1);
        }

        // 强制边界
        ratingElements.min.value = Math.min(max, Math.max(0, min)).toFixed(1);
        ratingElements.max.value = Math.max(min, Math.min(10, max)).toFixed(1);

        updateRatingDisplay();
    }

    // 更新显示
    function updateRatingDisplay() {
        if (ratingElements.allCheck.checked) {
            ratingElements.display.textContent = '评分范围：全部';
            return;
        }
        ratingElements.display.textContent = `评分范围：${ratingElements.min.value} - ${ratingElements.max.value}`;
    }

    // 初始化显示
    updateRatingDisplay();
});



//排序



//开始筛选


document.getElementById('searchButton').addEventListener('click', function() {
    // 收集标签
    const selectedTags = Array.from(document.querySelectorAll('.tag-item.active')).map(tag => tag.dataset.tagId);

    // 时间范围
    const allTimeChecked = document.getElementById('allTimeCheck').checked;
    let startTime = '';
    let endTime = '';
    if (!allTimeChecked) {
        startTime = document.querySelector('.start-month').value;
        endTime = document.querySelector('.end-month').value;
    }

    // 评分范围
    const allRatingChecked = document.getElementById('allRatingCheck').checked;
    let minRating = parseFloat(document.getElementById('minRating').value) || 0;
    let maxRating = parseFloat(document.getElementById('maxRating').value) || 10;

    // 排序方式
    const sortBy = document.querySelector('input[name="sortOption"]:checked').value;

     // 构建URL参数
    const params = new URLSearchParams();
    selectedTags.forEach(tag => params.append('tags', tag));
    params.append('all_time', allTimeChecked);
    params.append('start_time', startTime);
    params.append('end_time', endTime);
    params.append('all_rating', allRatingChecked);
    params.append('min_rating', minRating);
    params.append('max_rating', maxRating);
    params.append('sort_by', sortBy);

    // 跳转到结果页面
    window.location.href = `/filter/results/?${params.toString()}`;
});

// 辅助函数：获取CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
