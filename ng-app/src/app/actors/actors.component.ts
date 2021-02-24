import { ActorService } from '../actor.service';
import { Actor } from '../actor';

import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-actors',
  templateUrl: './actors.component.html',
  styleUrls: ['./actors.component.css']
})
export class ActorsComponent implements OnInit {

  // actors = ACTORS;
  actors!: Actor[];
  // selectedActor?: Actor;
  // onSelect(actor: Actor): void {
  //   this.selectedActor = actor;
  // }
  
  constructor(private actorService: ActorService) { }

  // getActors(): void {
  //   this.actors = this.actorService.getActors();
  // }

  getActors(): void {
    this.actorService.getActors()
        .subscribe(actors => this.actors = actors);
  }

  ngOnInit(): void {
    this.getActors();
  }

}
