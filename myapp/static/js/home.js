// 滚动监听
$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('.custom-navbar').addClass('scrolled');
    } else {
        $('.custom-navbar').removeClass('scrolled');
    }
});

function initProgressBars() {
    document.querySelectorAll('.progress-block').forEach(block => {
        const step = parseFloat(block.dataset.step) || 0;
        const total = parseFloat(block.dataset.total) || 1; // 防止除以0
        const percent = total === 0 ? 0 : Math.min((step / total) * 100, 100); // 最大100%

        // 更新进度条和百分比显示
        const fill = block.querySelector('.progress-fill');
        const percentText = block.querySelector('.progress-percent');
        if (fill) fill.style.width = `${percent}%`;
        if (percentText) percentText.textContent = `${percent.toFixed(1)}%`;
    });
}

// 页面加载时执行
document.addEventListener('DOMContentLoaded', initProgressBars);


// 评分
function renderAllRatings() {

    // 选择所有评分容器（包含private和public）
    document.querySelectorAll('.rating-item .stars').forEach(container => {
        const rating = parseFloat(container.dataset.rating) || 0;
        const total = parseFloat(container.dataset.total) || 10;
        const maxStars = 9;

        // 清空容器
        const starsContainer = container.querySelector('.stars-container');
        starsContainer.innerHTML = '';

        // 生成基础层（空心星）
        const baseLayer = document.createElement('div');
        baseLayer.className = 'star-base';
        baseLayer.innerHTML = '<i class="fas fa-star"></i>'.repeat(maxStars);

        // 生成填充层（实心星）
        const fillLayer = document.createElement('div');
        fillLayer.className = 'star-fill';
        fillLayer.style.width = `${(rating / total) * 100}%`;
        fillLayer.innerHTML = '<i class="fas fa-star active"></i>'.repeat(maxStars);

        // 组合元素
        starsContainer.appendChild(baseLayer);
        starsContainer.appendChild(fillLayer);

        // 更新文字显示
        const ratingText = container.querySelector('.rating-text');
        if (ratingText) ratingText.textContent = rating.toFixed(1);
    });
}


// 初始化执行
document.addEventListener('DOMContentLoaded', renderAllRatings);

// 初始化执行
// document.addEventListener('DOMContentLoaded', renderStars);


function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


// ============== 新增删除订阅逻辑 ============== //
document.addEventListener('DOMContentLoaded', () => {
    // 使用事件委托监听删除按钮点击
    document.body.addEventListener('click', async (e) => {
        const btn = e.target.closest('[data-action="delete"]');
        if (!btn) return;

        e.preventDefault();
        const recordId = btn.dataset.recordId;
        const animeId = btn.dataset.animeId; // 新增获取animeId用于后续恢复
        const workItem = btn.closest('.work-item');

        if (!confirm('确定要取消订阅吗？此操作不可撤销！')) return;

        try {
            const response = await fetch('/delete_record/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `record_id=${recordId}`
            });

            const data = await response.json();

            if (data.status === 'success') {
                // 修改按钮状态
                btn.textContent = '重新订阅';
                btn.classList.replace('btn-danger', 'btn-success');
                btn.dataset.action = 'resubscribe';
                btn.dataset.animeId = animeId; // 保留animeId用于重新订阅

                // 隐藏其他操作按钮
                workItem.querySelectorAll('.btn-action:not([data-action])').forEach(button => {
                    button.style.display = 'none';
                });
            } else {
                alert(`操作失败: ${data.msg}`);
            }
        } catch (error) {
            console.error('删除失败:', error);
            alert('网络请求异常，请检查控制台');
        }
    });
});

// ============== 新增重新订阅逻辑 ============== //
document.body.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action="resubscribe"]');
    if (!btn) return;

    e.preventDefault();
    const animeId = btn.dataset.animeId;
    const workItem = btn.closest('.work-item');

    // 获取评分和进度数据
    const rating = parseFloat(workItem.querySelector('.private-rating .stars').dataset.rating);
    const step = parseInt(workItem.querySelector('.progress-block').dataset.step);

    try {
        const response = await fetch('/resubscribe/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                anime_id: animeId,
                score_user: rating,
                step: step
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            // 修改按钮状态
            btn.textContent = '删除订阅';
            btn.classList.replace('btn-success', 'btn-danger');
            btn.dataset.action = 'delete';
            btn.dataset.recordId = data.record_id; // 更新为新的record_id


            // 显示其他操作按钮
            workItem.querySelectorAll('.btn-action:not([data-action])').forEach(button => {
                button.dataset.recordId = data.record_id; // ⭐️ 新增此行
                button.style.display = 'inline-block';
            });
        } else {
            alert(`操作失败: ${data.msg}`);
        }
    } catch (error) {
        console.error('重新订阅失败:', error);
        alert('网络请求异常，请检查控制台');
    }
});




//进度修改

// ============== 修改进度功能 ============== //
document.addEventListener('DOMContentLoaded', () => {
  // 点击"修改进度"按钮打开模态框
  document.querySelectorAll('#process-change').forEach(btn => {
    btn.addEventListener('click', function() {
      const recordId = this.dataset.recordId;
      const total = parseInt(this.dataset.total);
      const currentStep = parseInt(this.closest('.work-item')
                          .querySelector('.progress-block').dataset.step);

      // 填充模态框数据
      document.getElementById('modal-total').textContent = total;
      document.getElementById('newStep').value = currentStep;
      document.getElementById('newStep').setAttribute('max', total);

      // 显示模态框
      $('#progressModal').modal('show');

      // 绑定确定按钮事件（确保单次绑定）
      const confirmBtn = document.getElementById('confirmStepChange');
      const handleConfirm = async () => {
        const newStep = parseInt(document.getElementById('newStep').value);
        const errorDiv = document.getElementById('stepError');

        // 验证输入
        if (isNaN(newStep) || newStep < 0 || newStep > total) {
          errorDiv.textContent = `请输入 0-${total} 之间的整数`;
          return;
        }
        errorDiv.textContent = '';

        try {
          // 发送更新请求
          const response = await fetch('/update_step/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
              record_id: recordId,
              new_step: newStep
            })
          });

          const data = await response.json();

          if (data.status === 'success') {
            // 更新前端数据
            const progressBlock = document.querySelector(`.progress-block[data-step="${currentStep}"]`);
            progressBlock.dataset.step = newStep;
            initProgressBars(); // 重新初始化进度条
              console.log('====23')
            $('#progressModal').modal('hide');
          } else {
            alert(`更新失败: ${data.msg}`);
          }
        } catch (error) {
          console.error('请求异常:', error);
          alert('网络错误，请稍后重试');
        }
      };

      // 移除旧事件监听器，避免重复绑定
      confirmBtn.removeEventListener('click', handleConfirm);
      confirmBtn.addEventListener('click', handleConfirm);
    });
  });
});




//pingfen
// 在DOMContentLoaded事件监听器中新增以下代码
document.addEventListener('DOMContentLoaded', () => {
  // 点击"修改评分"按钮打开模态框
  document.querySelectorAll('#rate-change').forEach(btn => {
    btn.addEventListener('click', function() {
      const recordId = this.dataset.recordId;
      const currentRating = parseFloat(this.closest('.work-item')
                          .querySelector('.private-rating .stars').dataset.rating)

      // 填充模态框数据
      document.getElementById('newRating').value = currentRating;
      $('#ratingModal').modal('show');

      // 绑定确定按钮事件
      const confirmBtn = document.getElementById('confirmRatingChange');
      const handleConfirm = async () => {
        const newRating = parseFloat(document.getElementById('newRating').value);
        const errorDiv = document.getElementById('ratingError');

        // 输入验证
        if (isNaN(newRating) || newRating < 0 || newRating > 10) {
          errorDiv.textContent = '请输入0-10之间的数值';
          return;
        }
        errorDiv.textContent = '';

        try {
          const response = await fetch('/update_rating/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
              record_id: recordId,
              new_rating: newRating
            })
          });

          const data = await response.json();
          if (data.status === 'success') {
            // 更新前端显示
            const starsContainer = document.querySelector(`.work-item [data-record-id="${recordId}"]`)
                                  .closest('.work-item')
                                  .querySelector('.private-rating .stars');
            starsContainer.dataset.rating = newRating;
            renderAllRatings(); // 重新渲染所有评分
            $('#ratingModal').modal('hide');
          } else {
            alert(`更新失败: ${data.msg}`);
          }
        } catch (error) {
          console.error('请求异常:', error);
          alert('网络错误，请稍后重试');
        }
      };

      confirmBtn.removeEventListener('click', handleConfirm);
      confirmBtn.addEventListener('click', handleConfirm);
    });
  });
});