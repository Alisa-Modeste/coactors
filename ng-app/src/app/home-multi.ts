import { Actor } from "./actor";
import { Title } from "./title";

export interface HomeMulti {
    // titles: Title[];
    titles: Array<Title>;
    actors: Actor[];
}

