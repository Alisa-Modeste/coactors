import { Component, OnInit } from '@angular/core';

import { TitleService } from '../title.service';
import { Title } from '../title';

@Component({
  selector: 'app-titles',
  templateUrl: './titles.component.html',
  styleUrls: ['./titles.component.css']
})
export class TitlesComponent implements OnInit {

  titles!: Title[];

  constructor(private titleService: TitleService) { }


  getTitles(): void {
    this.titleService.getTitles()
        .subscribe(titles => this.titles = titles);
  }

  ngOnInit(): void {
    this.getTitles();
  }


}
