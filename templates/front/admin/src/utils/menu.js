const menu = {
    list() {
        return [{"backMenu":[{"child":[{"allButtons":["新增","查看","修改","删除"],"appFrontIcon":"cuIcon-cardboard","buttons":["新增","查看","修改","删除"],"menu":"用户","menuJump":"列表","tableName":"yonghu"}],"menu":"用户管理"},{"child":[{"allButtons":["新增","查看","修改","删除","商品价格","商品平均分","好评度","中评度","差评度","首页总数","首页统计","生成数据","爬取数据"],"appFrontIcon":"cuIcon-addressbook","buttons":["查看","删除","生成数据","爬取数据","修改"],"menu":"商品信息","menuJump":"列表","tableName":"shangpinxinxi"}],"menu":"商品信息管理"},{"child":[{"allButtons":["查看","修改"],"appFrontIcon":"cuIcon-addressbook","buttons":["查看","修改"],"menu":"系统简介","tableName":"systemintro"}],"menu":"系统管理"}],"frontMenu":[],"hasBack登录":"是","hasBackRegister":"否","hasFront登录":"否","hasFrontRegister":"否","roleName":"管理员","tableName":"users"},{"backMenu":[{"child":[{"allButtons":["新增","查看","修改","删除","商品价格","商品平均分","好评度","中评度","差评度","首页总数","首页统计","生成数据","爬取数据"],"appFrontIcon":"cuIcon-addressbook","buttons":["查看","爬取数据"],"menu":"商品信息","menuJump":"列表","tableName":"shangpinxinxi"}],"menu":"商品信息管理"}],"frontMenu":[],"hasBack登录":"是","hasBackRegister":"是","hasFront登录":"是","hasFrontRegister":"是","roleName":"用户","tableName":"yonghu"}]
    }
}
export default menu;
