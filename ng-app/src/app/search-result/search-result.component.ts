import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Actor } from '../actor'
import { SearchService } from '../search.service';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {
  @Input() actors?: Actor[];
  // @Input() ?: Actor;
  constructor(
    private route: ActivatedRoute,
    private searchService: SearchService
  ) { }

  ngOnInit(): void {
    let type = this.route.snapshot.queryParams['type'];

    if (type=="actor"){
      this.getActors();
    }
  }

  getActors(): void {
    let query = this.route.snapshot.queryParams['query']
    // let type = this.route.snapshot.queryParams['type']

    this.searchService.getActors(query)
      // .subscribe(actor => this.actor = actor);
      .subscribe(actors => {
        this.actors = actors
      
      });
  }
}
