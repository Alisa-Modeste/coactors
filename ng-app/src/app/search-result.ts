import { Actor } from './actor'

export interface SearchResult {
    unknown: boolean;
    results: Array<Actor|Actor>;
}

