---
title: '[coding] hexo教程'
date: 2020-09-17 17:49:07
tags:
- coding
---

## hexo 安装

1. GitHub创建个人仓库，仓库名应该为：`用户名.github.io`。

2. 安装 Git。

3. 将 Git 与 GitHub 帐号绑定：

   ```
   git config --global user.name <你的GitHub用户名>
   git config --global user.email <你的GitHub注册邮箱>
   ```

4. 生成 ssh 密钥文件：`ssh-keygen -t rsa -C <你的GitHub注册邮箱>`，然后三个回车即可。

5. 找到生成的.ssh的文件夹中的id_rsa.pub密钥，将内容全部复制。

6. 打开[GitHub_Settings_keys](https://link.zhihu.com/?target=https%3A//github.com/settings/keys) 页面，新建new SSH Key。Title为标题，任意填即可，将刚刚复制的id_rsa.pub内容粘贴进去，最后点击Add SSH key。

7. 安装 nodejs。

8. 安装 hexo：`npm install -g hexo-cli`

9. 初始化 hexo：`hexo init <hexo_root>`

10. 安装 pandoc：`npm install hexo-renderer-pandoc --save`

11. `npm install hexo-deployer-git --save`

### 常见错误

- hexo : 无法加载文件 C:\Users\zhbli\AppData\Roaming\npm\hexo.ps1，因为在此系统上禁止运行脚本。
  - 以管理员身份运行powershell，执行 `set-executionpolicy remotesigned`，输入 Y 即可。



## 本地部署

hexo s

## 添加自定义 css 样式

1. `cd themes\hexo-theme-next-7.8.0\source\css`

2. 创建并编辑自定义的样式文件 `custom.styl`
3. 在`main.styl`中添加`@import "custom.styl";`

## 自定义表格样式

在自定义 css 样式文件`custom.styl`中添加代码。如，设置表头不换行：

```
table th {
    white-space: nowrap; /*表头内容强制在一行显示*/
}
```

## 表格不换行

```
<span style="white-space:nowrap;">内容</span>
```

## hexo 本地与远程样式显示不一致

在浏览器按 `ctrl+F5` 强制刷新，即可将样式正确加载。原因：浏览器有缓存。