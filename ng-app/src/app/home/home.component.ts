import { Component, OnInit, Input } from '@angular/core';

import { Actor } from '../actor'
import { HomeService } from '../home.service';
import { Title } from '../title';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  @Input() actors?: Actor[];
  @Input() titles?: Title[];
  constructor(private homeService: HomeService) { }

  ngOnInit(): void {
    this.getValues();
  }

  getValues(): void {

    this.homeService.getValues()

      .subscribe(results => {

        this.titles = results.titles;
        this.actors = results.actors;
      
      });
  }

}
