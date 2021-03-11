export interface Title {
    uid: string;
    title: string;
    cast: Array<actors>;
    released: number;
}

interface actors { 
    uid: string,
    name: string
 }
