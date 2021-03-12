export interface Actor {
    uid: string;
    name: string;
    // titles: Array<Object>;
    titles: Array<titles>;
    coactors: Array<coactors>;
    group_members: Array<group_members>;
}

interface titles { 
    title:string,
    uid:string,
    released:number
 }

interface coactors {
    uid: string,
    name: string
    // titles: Array<Object>;
    
}

interface group_members {
    uid: string,
    name: string    
}