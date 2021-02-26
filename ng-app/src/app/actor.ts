export interface Actor {
    uid: string;
    name: string;
    // titles: Array<Object>;
    titles: Array<titles>;
    coactors: Array<coactors>;
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