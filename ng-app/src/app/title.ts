export interface Title {
    uid: string;
    title: string;
    cast: Array<actors>;
    released: number;
    title_type: string;
}

interface actors { 
    uid: string,
    name: string
 }
