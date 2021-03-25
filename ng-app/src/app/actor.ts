export interface Actor {
    uid: string;
    name: string;
    // titles: Array<Object>;
    titles: Array<titles>;
    coactors: Array<coactors>;
    group_members: Array<group_members>;
    children_known: string;
}

interface titles { 
    title:string,
    uid:string,
    released:number
 }

interface coactors {
    uid: string,
    name: string
    children_known: string
}

interface group_members {
    uid: string,
    name: string,
    children_known: string
}