<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20261023013035 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE contrainte (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, type VARCHAR(30) NOT NULL, valeur INTEGER DEFAULT NULL, projet_id INTEGER NOT NULL, tache_a_id INTEGER NOT NULL, tache_b_id INTEGER DEFAULT NULL, CONSTRAINT FK_17925A70C18272 FOREIGN KEY (projet_id) REFERENCES projet (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE, CONSTRAINT FK_17925A7049ED371E FOREIGN KEY (tache_a_id) REFERENCES tache (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE, CONSTRAINT FK_17925A705B5898F0 FOREIGN KEY (tache_b_id) REFERENCES tache (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE)');
        $this->addSql('CREATE INDEX IDX_17925A70C18272 ON contrainte (projet_id)');
        $this->addSql('CREATE INDEX IDX_17925A7049ED371E ON contrainte (tache_a_id)');
        $this->addSql('CREATE INDEX IDX_17925A705B5898F0 ON contrainte (tache_b_id)');
        $this->addSql('CREATE TABLE projet (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom VARCHAR(255) NOT NULL, description CLOB DEFAULT NULL, date_creation DATETIME NOT NULL)');
        $this->addSql('CREATE TABLE tache (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, description VARCHAR(255) NOT NULL, duree INTEGER NOT NULL, projet_id INTEGER NOT NULL, CONSTRAINT FK_93872075C18272 FOREIGN KEY (projet_id) REFERENCES projet (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE)');
        $this->addSql('CREATE INDEX IDX_93872075C18272 ON tache (projet_id)');
        $this->addSql('CREATE TABLE tache_precedente (tache_id INTEGER NOT NULL, precedente_id INTEGER NOT NULL, PRIMARY KEY (tache_id, precedente_id), CONSTRAINT FK_E52AAACDD2235D39 FOREIGN KEY (tache_id) REFERENCES tache (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE, CONSTRAINT FK_E52AAACD562D9ABA FOREIGN KEY (precedente_id) REFERENCES tache (id) ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE)');
        $this->addSql('CREATE INDEX IDX_E52AAACDD2235D39 ON tache_precedente (tache_id)');
        $this->addSql('CREATE INDEX IDX_E52AAACD562D9ABA ON tache_precedente (precedente_id)');
        $this->addSql('CREATE TABLE messenger_messages (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, body CLOB NOT NULL, headers CLOB NOT NULL, queue_name VARCHAR(190) NOT NULL, created_at DATETIME NOT NULL, available_at DATETIME NOT NULL, delivered_at DATETIME DEFAULT NULL)');
        $this->addSql('CREATE INDEX IDX_75EA56E0FB7336F0E3BD61CE16BA31DBBF396750 ON messenger_messages (queue_name, available_at, delivered_at, id)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('DROP TABLE contrainte');
        $this->addSql('DROP TABLE projet');
        $this->addSql('DROP TABLE tache');
        $this->addSql('DROP TABLE tache_precedente');
        $this->addSql('DROP TABLE messenger_messages');
    }
}
