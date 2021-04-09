import { query } from '@angular/animations';
import { Component, ViewChild, ElementRef, Renderer2, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { SearchService } from './search.service';
import { baseUrl } from './base-url';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Have We Worked Together?';
  routeSegment = "";
  homepage:string = baseUrl + "/";

  // // @ViewChild('hello', { static: false }) navbar!: ElementRef;
  @ViewChild('theNavbar') navbar!: ElementRef;
  @ViewChild('navbarOffset') navbarOffset!: ElementRef;
  @ViewChild('searchTerm') searchTerm!: HTMLInputElement;
  

  // // constructor(private el: ElementRef) {
  // constructor(private navbarOffset: ElementRef, private navbar: ElementRef, private renderer: Renderer2) {
    constructor(
      private renderer: Renderer2,
      private searchService: SearchService,
      private router: Router,
      private http: HttpClient
    ) {
  
        // so components can be updated when a different param is used
        this.router.routeReuseStrategy.shouldReuseRoute = function () {
          return false;
        };

  }

  ngOnInit() {
    this.http.get<any>(this.homepage);
  }

  ngAfterViewInit() {

    this.resizeMe()
  }

  ngAfterContentChecked(): void{
    this.routeSegment = this.router.routerState.snapshot.url;
    this.routeSegment = this.routeSegment.split("/")[1]
  }

  resizeMe() {

    let currentHeight = this.navbar.nativeElement.clientHeight
    this.renderer.setStyle(this.navbarOffset.nativeElement, 'height', currentHeight+20);
  }

  @HostListener('window:resize') 
    onResize() {
      this.resizeMe()

  }

    getActors(searchTerm: string) {
      // this.searchService.getActors()
      //   .subscribe(actors => this.actors = actors);

        // this.router.navigateByUrl('/actor_search');

        this.router.navigateByUrl(
          this.router.createUrlTree(
            // ['actor_search'], {queryParams: {"query": "sana"}}
            // ['search'], {queryParams: {"query": "sana", "type": "actor"}}

            ['search'], {queryParams: {"query": searchTerm, "type": "actor"}}
          )
        );
    }

    getTitles(searchTerm: string) {
      this.router.navigateByUrl(
        this.router.createUrlTree(
          // ['actor_search'], {queryParams: {"query": "sana"}}
          // ['search'], {queryParams: {"query": "sana", "type": "actor"}}

          ['search'], {queryParams: {"query": searchTerm, "type": "title"}}
        )
      );
    }
}
