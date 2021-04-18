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
  @Input() known?: boolean;
  @Input() query?: string;

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
    let more = this.route.snapshot.queryParams['more']

    this.searchService.getActors(query, more)
      .subscribe(results => {

        this.actors = results.results;
        this.known = results.known;
        this.query = query;
      
      });
  }

  getTitles(): void {
    let query = this.route.snapshot.queryParams['query']
    let more = this.route.snapshot.queryParams['more']

    this.searchService.getTitles(query, more)
      .subscribe(results => {

        this.titles = results.results;
        this.known = results.known;
        this.query = query;
      
      });
  }
}
