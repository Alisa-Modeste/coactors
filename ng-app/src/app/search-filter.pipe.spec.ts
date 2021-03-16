import { SearchFilterPipe } from './search-filter.pipe';

describe('SearchFilterPipe', () => {
  it('create an instance', () => {
    const pipe = new SearchFilterPipe();
    expect(pipe).toBeTruthy();
  });

  it('should filter by search term', () => {
    const searchPipe = new SearchFilterPipe();
    console.log("searchPipe")
    console.log(searchPipe)
    let result = searchPipe.transform([{"name":"Adam"}, {"name":"Bianca"}, {"name":"Vicki"}, {"name":"Roxanna"}], "a");
    
    console.log("result.length")
    console.log(result.length)
    expect(result.length).toEqual(3);
    console.log(result)
    expect(result).toEqual([{"name":"Adam"}, {"name":"Bianca"}, {"name":"Roxanna"}]);
  });
});
