源码目录介绍

``` text
./js
├── base                                   // 定义游戏开发基础类
│   ├── button.js                          // 游戏内可点击图片类
│   └── eventUtil.js                       // 处理点击事件的类
├── libs
│   ├── bezier.js                          // 用于进行淡入淡出动画的类库 https://github.com/gre/bezier-easing
│   ├── symbol.js                          // ES6 Symbol简易兼容
│   └── weapp-adapter.js                   // 小游戏适配器
├── models
│   └── piece.js                           // 拼图方块类
├── runtime
│   ├── background.js                      // 背景类
│   ├── gameInfo.js                        // 游戏菜单、按钮和分数
│   ├── gameMap.js                         // 用于提供游戏的随机地图
│   └── music.js                           // 全局音效管理器
├── databus.js                             // 管控游戏状态
└── main.js                                // 游戏入口主函数

```
