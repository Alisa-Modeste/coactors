import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
// import {MatTabsModule} from '@angular/material/tabs';

import { Title } from '../title'
import { TitleService } from '../title.service';
import { MessageService } from '../message.service';
import { TitlesComponent } from '../titles/titles.component';

@Component({
  selector: 'app-title-detail',
  templateUrl: './title-detail.component.html',
  styleUrls: ['./title-detail.component.css']
})
export class TitleDetailComponent implements OnInit {

  @Input() title?: Title;

  constructor(
    private route: ActivatedRoute,
    private titleService: TitleService,
    private location: Location,
    private router: Router,
    private messageService: MessageService
  ) {

    // so components can be updated when a different param is used
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };

  }


  ngOnInit(): void {
    this.getTitle();
  }

  ngOnChanges(): void {
    this.getTitle();
  }

  getTitle(): void {
    const uid = ""+this.route.snapshot.paramMap.get('uid');
    const known = this.route.snapshot.queryParams['k']
    const title_type = this.route.snapshot.queryParams['title_type']
    const childrenKnown = this.route.snapshot.queryParams['ck']
    console.log("uid:" + uid)
    console.log( this.route)
    this.titleService.getTitle(uid, known, title_type, childrenKnown)
      // .subscribe(actor => this.actor = actor);
      .subscribe(title => {
        this.title = title

        this.messageService.clear();

  });

}

}
