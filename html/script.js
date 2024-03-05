const body = document.querySelector('body')
const sidebar = body.querySelector('.sidebar')
const toggle = body.querySelector('.toggle')
const showImgList = body.querySelector('.show-img-list')
const page1 = body.querySelector('.page1')
const page2 = body.querySelector('.page2')
const page3 = body.querySelector('.page3')
const imageSearch = body.querySelector('#image-search')
const featureExtraction = body.querySelector('#feature-extraction')
const setting = body.querySelector('#setting')
const featureFileStorageAddress = body.querySelector('#featureFileStorageAddress')
const searchSimilarImagesNumber = body.querySelector('#searchSimilarImagesNumber')

console.log(imageSearch);
console.log(featureExtraction);

// 侧边栏伸缩按钮点击事件
toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close')
})

// 侧边栏图片搜索点击事件
imageSearch.addEventListener('click', () => {
    if (page1.classList.contains('hidden-page')) {
        page1.classList.remove('hidden-page')
    }
    if (!page2.classList.contains('hidden-page')) {
        page2.classList.add('hidden-page')
    }
    if (!page3.classList.contains('hidden-page')) {
        page3.classList.add('hidden-page')
    }
})

// 侧边栏特征提取点击事件
featureExtraction.addEventListener('click', () => {
    if (page2.classList.contains('hidden-page')) {
        page2.classList.remove('hidden-page')
    }
    if (!page1.classList.contains('hidden-page')) {
        page1.classList.add('hidden-page')
    }
    if (!page3.classList.contains('hidden-page')) {
        page3.classList.add('hidden-page')
    }
})

// 设置按钮点击事件
setting.addEventListener('click', () => {
    if (page3.classList.contains('hidden-page')) {
        page3.classList.remove('hidden-page')
    }
    if (!page1.classList.contains('hidden-page')) {
        page1.classList.add('hidden-page')
    }
    if (!page2.classList.contains('hidden-page')) {
        page2.classList.add('hidden-page')
    }
})

/**
 * 初始化加载配置文件
 */
document.addEventListener('DOMContentLoaded', function () {
    loadImg()
});

function loadImg() {
    for (let i = 1; i < 40; i++) {
        const cell = document.createElement('div')
        cell.classList.add('cell')
        cell.innerHTML = `
		    <img src="" />
		  </div>
		`
        showImgList.appendChild(cell)
    }
}

window.addEventListener('pywebviewready', function () {
    featureFileStorageAddress.value = 'pywebview is ready'
})