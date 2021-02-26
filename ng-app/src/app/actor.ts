export interface Actor {
    uid: string;
    name: string;
    titles: Array<Object>;
    
}

interface titles { 
    title:string, 
    uid:string, 
    released:number
 } 