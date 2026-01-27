/**
 * G-AI SYSTEM LOADER // VER 1.7 (Stable Random Text)
 * 每次跳转随机选一句骚话，但在加载过程中文字保持静止，不闪烁。
 */

(function() {
    // --- 0. 预判逻辑 (无缝衔接) ---
    const FLAG_KEY = 'g_ai_internal_nav';
    const isInternalNav = sessionStorage.getItem(FLAG_KEY);
    
    const isBack = (function() {
        const nav = performance.getEntriesByType("navigation");
        if (nav.length > 0 && nav[0].type === 'back_forward') return true;
        if (window.performance && window.performance.navigation.type === 2) return true;
        return false;
    })();

    const shouldShowInit = !isInternalNav && !isBack;
    const initialClass = shouldShowInit ? 'active' : 'hidden';

    if (isInternalNav) sessionStorage.removeItem(FLAG_KEY);

    // --- 1. 注入 CSS ---
    const style = document.createElement('style');
    style.innerHTML = `
        #g-loader {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: #000;
            z-index: 99999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', monospace;
            color: #00ff41;
            transition: opacity 0.5s ease;
            pointer-events: none;
        }
        
        #g-loader.active {
            pointer-events: all !important;
            opacity: 1;
        }

        #g-loader.hidden {
            opacity: 0;
            pointer-events: none !important;
        }

        .loader-text {
            font-size: 1.2rem;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px #00ff41;
            min-height: 1.5em;
            font-weight: bold;
        }

        .loader-bar {
            width: 300px;
            height: 4px;
            background: #111;
            position: relative;
            overflow: hidden;
        }

        .loader-progress {
            width: 0%;
            height: 100%;
            background: #00ff41;
            box-shadow: 0 0 15px #00ff41;
            transition: width 0.2s linear;
        }
    `;
    document.head.appendChild(style);

    // --- 2. 注入 DOM ---
    const loaderHTML = `
        <div id="g-loader" class="${initialClass}">
            <div class="loader-text" id="loader-msg"></div> 
            <div class="loader-bar">
                <div class="loader-progress" id="loader-bar"></div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loaderHTML);

    const loader = document.getElementById('g-loader');
    const bar = document.getElementById('loader-bar');
    const msg = document.getElementById('loader-msg');

    // --- 3. 核心动画函数 ---
    function runLoader(text, callback, duration = 800) {
        // 直接显示传入的文字 (不再变动)
        msg.innerText = text;
        
        bar.style.width = '0%';
        void loader.offsetWidth; // 强制重绘
        
        loader.classList.remove('hidden');
        loader.classList.add('active');
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;
            
            bar.style.width = `${progress}%`;

            if (progress === 100) {
                clearInterval(interval);
                setTimeout(() => {
                    if (callback) callback(); 
                    else {
                        loader.classList.remove('active');
                        loader.classList.add('hidden');
                    }
                }, 200);
            }
        }, duration / 10);
    }

    // --- 4. 初始化 (系统启动) ---
    if (shouldShowInit) {
        runLoader("SYSTEM_INIT...", null, 1000);
    }

    // --- 5. 点击拦截 (随机抽取一句，然后锁定) ---
    // G-AI 专用术语库：统一 LINKING 结尾，对应系统各大模块
    const jumpPhrases = [
        "G-PROTOCOL LINKING...",     // 连接 G协议 (总线)
        "AGENT SWARM LINKING...",    // 连接 智能体蜂群 (执行层)
        "INTENT NODE LINKING...",    // 连接 意图节点 (分发层)
        "HIVE MIND LINKING...",      // 连接 蜂巢思维 (知识库)
        "SUPPLY CHAIN LINKING...",   // 连接 供应链 (丐物)
        "NEURAL NET LINKING...",     // 连接 神经网络 (AI核心)
        "CORE UPLINK LINKING..."     // 连接 核心上行链路 (权限)
    ];

    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.href) {
            if (link.href.includes('#') || link.target === '_blank') return;
            if (link.href === window.location.href) return;

            e.preventDefault();

            sessionStorage.setItem(FLAG_KEY, 'true');
            
            // 【关键修改】在这里随机选好一句话，传进去
            const randomText = jumpPhrases[Math.floor(Math.random() * jumpPhrases.length)];
            
            runLoader(randomText, () => {
                window.location.href = link.href;
            }, 500);
        }
    });

    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            loader.classList.remove('active');
            loader.classList.add('hidden');
        }
    });

})();