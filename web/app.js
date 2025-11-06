// Configuration
const API_BASE_URL = 'http://localhost:8000';
const USER_ID = 1; // Demo user ID

// Global state
let currentPage = 'dashboard';
let allFoodItems = [];
let currentFilter = 'all';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboard();
    setDefaultDate();
});

// Navigation
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-page');
            navigateToPage(page);
        });
    });
}

function navigateToPage(pageName) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === pageName) {
            link.classList.add('active');
        }
    });

    // Update pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(`${pageName}-page`).classList.add('active');

    currentPage = pageName;

    // Load page data
    switch(pageName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'fridge':
            loadFridgeItems();
            break;
        case 'recipes':
            loadRecipes();
            break;
        case 'shopping':
            loadShoppingList();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const stats = await fetchAPI(`/api/stats/${USER_ID}`);
        updateStats(stats);

        const items = await fetchAPI(`/api/items/expiring/${USER_ID}?days=3`);
        updateUrgentItems(items);

        updateCategoryChart(stats.category_breakdown);
    } catch (error) {
        showToast('加载数据失败', 'error');
    }
}

function updateStats(stats) {
    document.getElementById('totalItems').textContent = stats.total_items;
    document.getElementById('expiringToday').textContent = stats.expiring_today;
    document.getElementById('expiringSoon').textContent = stats.expiring_within_3_days;
    document.getElementById('freshItems').textContent = stats.fresh_items;
}

function updateUrgentItems(items) {
    const alertDiv = document.getElementById('urgentAlert');
    const listDiv = document.getElementById('urgentItemsList');

    if (items.length === 0) {
        alertDiv.style.display = 'none';
        return;
    }

    alertDiv.style.display = 'block';
    listDiv.innerHTML = items.map(item => {
        const daysText = item.days_left === 0 ? '今天到期！' :
                        item.days_left < 0 ? '已过期' :
                        `还剩 ${item.days_left} 天`;
        return `
            <div class="urgent-item">
                <strong>${item.food_name}</strong> (${item.quantity}${item.quantity_unit}) - ${daysText}
            </div>
        `;
    }).join('');
}

function updateCategoryChart(categories) {
    const chartDiv = document.getElementById('categoryChart');

    if (!categories || Object.keys(categories).length === 0) {
        chartDiv.innerHTML = '<p class="empty-state">暂无数据</p>';
        return;
    }

    const total = Object.values(categories).reduce((sum, val) => sum + val, 0);

    chartDiv.innerHTML = Object.entries(categories).map(([category, count]) => {
        const percentage = (count / total * 100).toFixed(0);
        return `
            <div class="category-item">
                <div class="category-label">${category}</div>
                <div class="category-bar">
                    <div class="category-bar-fill" style="width: ${percentage}%">
                        ${count}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function refreshDashboard() {
    loadDashboard();
    showToast('数据已刷新', 'success');
}

// Fridge Items
async function loadFridgeItems() {
    try {
        const items = await fetchAPI(`/api/items/${USER_ID}`);
        allFoodItems = items;
        displayFoodItems(items);
    } catch (error) {
        showToast('加载食材失败', 'error');
    }
}

function displayFoodItems(items) {
    const container = document.getElementById('fridgeItems');

    if (items.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <p>冰箱里还没有食材</p>
            </div>
        `;
        return;
    }

    container.innerHTML = items.map(item => {
        const urgencyClass = item.urgency_level;
        const badgeClass = `badge-${urgencyClass}`;
        const urgencyText = getUrgencyText(item.urgency_level, item.days_left);
        const urgencyEmoji = getUrgencyEmoji(item.urgency_level);

        return `
            <div class="food-card ${urgencyClass}">
                <div class="food-header">
                    <div>
                        <div class="food-name">${urgencyEmoji} ${item.food_name}</div>
                        <div class="food-meta">${item.category} • ${item.quantity}${item.quantity_unit}</div>
                    </div>
                    <span class="food-badge ${badgeClass}">${urgencyText}</span>
                </div>
                <div class="food-expiry">
                    ${formatExpiry(item.expiration_date, item.days_left)}
                </div>
                <div class="food-actions">
                    <button class="btn btn-success btn-sm" onclick="markAsConsumed(${item.id})">
                        ✅ 已吃完
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteItem(${item.id})">
                        🗑️ 删除
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function filterItems(filter) {
    currentFilter = filter;

    // Update button states
    document.querySelectorAll('[data-filter]').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-filter') === filter) {
            btn.classList.add('active');
        }
    });

    let filteredItems = allFoodItems;

    if (filter === 'urgent') {
        filteredItems = allFoodItems.filter(item =>
            ['expired', 'today', 'urgent'].includes(item.urgency_level)
        );
    } else if (filter === 'fresh') {
        filteredItems = allFoodItems.filter(item =>
            ['fresh', 'warning'].includes(item.urgency_level)
        );
    }

    displayFoodItems(filteredItems);
}

async function markAsConsumed(itemId) {
    try {
        await fetchAPI(`/api/items/consume/${itemId}`, 'PUT');
        showToast('已标记为已吃完', 'success');
        loadFridgeItems();
        if (currentPage === 'dashboard') loadDashboard();
    } catch (error) {
        showToast('操作失败', 'error');
    }
}

async function deleteItem(itemId) {
    if (!confirm('确定要删除这个食材吗？')) return;

    try {
        await fetchAPI(`/api/items/${itemId}`, 'DELETE');
        showToast('已删除', 'success');
        loadFridgeItems();
        if (currentPage === 'dashboard') loadDashboard();
    } catch (error) {
        showToast('删除失败', 'error');
    }
}

// Recipes
async function loadRecipes() {
    try {
        const recipes = await fetchAPI(`/api/recipes/recommend/${USER_ID}?limit=10`);
        displayRecipes(recipes);
    } catch (error) {
        showToast('加载食谱失败', 'error');
    }
}

function displayRecipes(recipes) {
    const container = document.getElementById('recipesList');

    if (recipes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">👨‍🍳</div>
                <p>暂无食谱推荐</p>
            </div>
        `;
        return;
    }

    container.innerHTML = recipes.map(recipe => {
        const matchRate = recipe.match_rate || 0;
        const missingCount = recipe.missing_ingredients?.length || 0;
        const totalTime = (recipe.prep_time || 0) + (recipe.cook_time || 0);

        return `
            <div class="recipe-card">
                <div class="recipe-header">
                    <div class="recipe-title">${recipe.name_cn || recipe.name}</div>
                    <div class="recipe-subtitle">${recipe.name}</div>
                </div>

                <div class="recipe-match">
                    <div class="match-bar">
                        <div class="match-bar-fill" style="width: ${matchRate}%"></div>
                    </div>
                    <div class="match-percentage">${matchRate.toFixed(0)}%</div>
                </div>

                <div class="recipe-info">
                    ⏱️ ${totalTime} 分钟 | 🍽️ ${recipe.category || '家常菜'}
                </div>

                ${missingCount === 0 ?
                    '<div class="ingredients-status" style="color: var(--success);">✅ 所有食材齐全！</div>' :
                    `<div class="ingredients-status" style="color: var(--warning);">
                        ⚠️ 还缺少 ${missingCount} 样食材：
                        <div class="missing-list">${recipe.missing_ingredients.join(', ')}</div>
                    </div>`
                }

                ${missingCount > 0 ?
                    `<button class="btn btn-secondary btn-sm" onclick="addMissingToShoppingList(${JSON.stringify(recipe.missing_ingredients).replace(/"/g, '&quot;')}, '${recipe.name_cn}')">
                        🛒 添加缺失食材到购物清单
                    </button>` : ''
                }
            </div>
        `;
    }).join('');
}

function addMissingToShoppingList(ingredients, recipeName) {
    ingredients.forEach(async (ingredient) => {
        try {
            await fetchAPI(`/api/shopping/${USER_ID}`, 'POST', {
                item_name: ingredient,
                quantity: 1,
                reason: `${recipeName}需要`
            });
        } catch (error) {
            console.error('Failed to add ingredient:', ingredient);
        }
    });
    showToast(`已添加 ${ingredients.length} 样食材到购物清单`, 'success');
}

// Shopping List
async function loadShoppingList() {
    try {
        const items = await fetchAPI(`/api/shopping/${USER_ID}?include_purchased=true`);
        displayShoppingList(items);
    } catch (error) {
        showToast('加载购物清单失败', 'error');
    }
}

function displayShoppingList(items) {
    const pendingList = document.getElementById('pendingItemsList');
    const purchasedList = document.getElementById('purchasedItemsList');

    const pending = items.filter(item => item.is_purchased === 0);
    const purchased = items.filter(item => item.is_purchased === 1);

    pendingList.innerHTML = pending.length > 0 ?
        pending.map(item => createShoppingItemHTML(item)).join('') :
        '<p class="empty-state">购物清单为空</p>';

    purchasedList.innerHTML = purchased.length > 0 ?
        purchased.map(item => createShoppingItemHTML(item)).join('') :
        '<p class="empty-state">暂无已购买商品</p>';
}

function createShoppingItemHTML(item) {
    return `
        <div class="shopping-item ${item.is_purchased ? 'purchased' : ''}">
            <input type="checkbox"
                   class="shopping-checkbox"
                   ${item.is_purchased ? 'checked' : ''}
                   onchange="togglePurchased(${item.id}, this.checked)">
            <div class="shopping-item-content">
                <div class="shopping-item-name">
                    ${item.item_name} - ${item.quantity}${item.quantity_unit || ''}
                </div>
                ${item.reason ? `<div class="shopping-item-reason">${item.reason}</div>` : ''}
            </div>
        </div>
    `;
}

async function togglePurchased(itemId, isPurchased) {
    try {
        if (isPurchased) {
            await fetchAPI(`/api/shopping/purchase/${itemId}`, 'PUT');
        }
        loadShoppingList();
    } catch (error) {
        showToast('操作失败', 'error');
    }
}

function showAddShoppingItemModal() {
    document.getElementById('shoppingModal').classList.add('active');
}

function closeModal() {
    document.getElementById('shoppingModal').classList.remove('active');
    document.getElementById('addShoppingForm').reset();
}

async function addShoppingItem(event) {
    event.preventDefault();

    const itemData = {
        item_name: document.getElementById('shoppingItemName').value,
        quantity: parseInt(document.getElementById('shoppingQuantity').value),
        quantity_unit: document.getElementById('shoppingUnit').value,
        reason: document.getElementById('shoppingReason').value
    };

    try {
        await fetchAPI(`/api/shopping/${USER_ID}`, 'POST', itemData);
        showToast('已添加到购物清单', 'success');
        closeModal();
        loadShoppingList();
    } catch (error) {
        showToast('添加失败', 'error');
    }
}

// Add Food Item
function setDefaultDate() {
    const dateInput = document.getElementById('expirationDate');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 7);
    dateInput.value = tomorrow.toISOString().split('T')[0];
}

async function addFoodItem(event) {
    event.preventDefault();

    const itemData = {
        food_name: document.getElementById('foodName').value,
        category: document.getElementById('category').value,
        quantity: parseInt(document.getElementById('quantity').value),
        quantity_unit: document.getElementById('quantityUnit').value,
        expiration_date: new Date(document.getElementById('expirationDate').value).toISOString()
    };

    try {
        await fetchAPI(`/api/items/${USER_ID}`, 'POST', itemData);
        showToast('食材已添加！', 'success');
        document.getElementById('addItemForm').reset();
        setDefaultDate();

        // Refresh data if on fridge or dashboard page
        if (currentPage === 'fridge') loadFridgeItems();
        if (currentPage === 'dashboard') loadDashboard();
    } catch (error) {
        showToast('添加失败：' + error.message, 'error');
    }
}

// Utility Functions
async function fetchAPI(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Request failed');
    }

    return response.json();
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function getUrgencyText(urgencyLevel, daysLeft) {
    switch (urgencyLevel) {
        case 'expired': return '已过期';
        case 'today': return '今天';
        case 'urgent': return `${daysLeft}天`;
        case 'warning': return `${daysLeft}天`;
        case 'fresh': return '新鲜';
        default: return '-';
    }
}

function getUrgencyEmoji(urgencyLevel) {
    const emojiMap = {
        'expired': '❌',
        'today': '⚠️',
        'urgent': '🟡',
        'warning': '🟢',
        'fresh': '✅'
    };
    return emojiMap[urgencyLevel] || '📦';
}

function formatExpiry(expirationDate, daysLeft) {
    const date = new Date(expirationDate);
    const dateStr = date.toLocaleDateString('zh-CN');

    if (daysLeft < 0) {
        return `${dateStr} (已过期 ${Math.abs(daysLeft)} 天)`;
    } else if (daysLeft === 0) {
        return `${dateStr} (今天到期！)`;
    } else {
        return `${dateStr} (还剩 ${daysLeft} 天)`;
    }
}
