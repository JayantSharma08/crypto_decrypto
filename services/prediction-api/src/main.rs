
use actix_web::{ HttpServer, App, web, Responder, HttpResponse };

async fn health() -> impl Responder {
    println!("Health endpoint was hit!");
    HttpResponse::Ok().body("Hey there!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Hello, world!");
    
    HttpServer::new(|| {
        App::new()
            .route("/health", web::get().to(health))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
