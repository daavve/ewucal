var setting = {
    async: {
        enable: true,
        url:'/ajax/get_root_tree',
        autoParam:["id", "name=n", "level=lv"],
        dataFilter: filter
    },
    callback: {
        beforeClick: launchWindow
    }
};

function launchWindow(treeId, treeNode){
    if (!treeNode.isParent) {
        let str = treeNode.id.substring(8);
        console.log(str);
        $.jsPanel({
            contentIframe: {
                src: 'page/' + str
            }
        });
        return false;
    } else {
        return true;
    }
}



function filter(treeId, parentNode, childNodes) {
    if (!childNodes) return null;
    for (var i=0, l=childNodes.length; i<l; i++) {
        childNodes[i].name = childNodes[i].name.replace(/\.n/g, '.');
    }
    return childNodes;
}


$(document).ready(function(){
    $.fn.zTree.init($("#treeDemo"), setting);
});
