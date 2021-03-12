import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Actor } from '../actor'
import { SearchService } from '../search.service';
import { Title } from '../title';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {
  @Input() actors?: Actor[];
  @Input() titles?: Title[];
  @Input() unknown?: boolean;
  // @Input() ?: Actor;
  constructor(
    private route: ActivatedRoute,
    private searchService: SearchService,
    private router: Router
      ) {
  
        // so components can be updated when a different param is used
        this.router.routeReuseStrategy.shouldReuseRoute = function () {
          return false;
        };
    }

  ngOnInit(): void {
    let type = this.route.snapshot.queryParams['type'];

    if (type=="actor"){
      this.getActors();
    }
    else if(type=="title"){
      this.getTitles();
    }
  }

  getActors(): void {
    let query = this.route.snapshot.queryParams['query']
    // let type = this.route.snapshot.queryParams['type']

    this.searchService.getActors(query)
      // .subscribe(actor => this.actor = actor);
      .subscribe(results => {
        console.log('the results are...')
        console.log(results)
        // this.actors = actors
        this.actors = results.results;
        console.log("this actors")
        console.log(this.actors)
        this.unknown = results.unknown;
      
      });
  }

  getTitles(): void {
    let query = this.route.snapshot.queryParams['query']
    // let type = this.route.snapshot.queryParams['type']

    this.searchService.getTitles(query)
      // .subscribe(actor => this.actor = actor);
      .subscribe(results => {
        console.log('the results are...')
        console.log(results)
        // this.actors = actors
        this.titles = results.results;
        console.log("this actors")
        console.log(this.titles)
        this.unknown = results.unknown;
      
      });
  }
}
