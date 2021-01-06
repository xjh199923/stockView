import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/dashboard',
                    component: () => import(/* webpackChunkName: "dashboard" */ '../components/page/Dashboard.vue'),
                    meta: { title: '系统首页' }
                },
                {
                    path: '/table',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/BaseTable.vue'),
                    meta: { title: '基础表格' }
                },
                {
                    // K线图
                    path: '/k_line',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/K_line.vue'),
                    meta: { title: 'K线图', permission: true }
                },
                {
                    //成交额成交量
                    path: "stockvolume",
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/StockVolume.vue'),
                    meta: { title: '成交额成交量', permission: true }
                },
                {
                    // 16_17年成交量对比图
                    path: '/volumeContrast16_17',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/VolumeContrast16_17.vue'),
                    meta: { title: '成交量分析', permission: true }
                },
                {
                    // 平均成交量前n支股票对比图
                    path: '/volumeFirstN',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/VolumeFirstN.vue'),
                    meta: { title: '成交量前列', permission: true }
                },
                {
                    // 平均成交量前n支股票稳定性分析
                    path: '/boxplot',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/Boxplot.vue'),
                    meta: { title: '稳定性分析', permission: true }
                },
                {
                    // 测试
                    path: '/predict',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/Predict.vue'),
                    meta: { title: '成交额预测分析', permission: true }
                },
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
    ]
});
