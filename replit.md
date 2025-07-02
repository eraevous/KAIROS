# Government Document Generator

## Overview

This is a full-stack web application designed for government agencies to generate procurement documents using AI-powered automation. The system provides secure document creation for RFPs (Request for Proposals), SOWs (Statement of Work), and procurement memorandums with integrated document management and audit capabilities.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and optimized builds
- **UI Framework**: Shadcn/UI components built on Radix UI primitives
- **Styling**: Tailwind CSS with custom government color schemes
- **State Management**: TanStack Query for server state management
- **Routing**: Wouter for lightweight client-side routing
- **Form Handling**: React Hook Form with Zod validation

### Backend Architecture
- **Runtime**: Node.js with Express.js server
- **Language**: TypeScript throughout the stack
- **API Design**: RESTful API with JSON responses
- **File Upload**: Multer middleware for document handling
- **Session Management**: In-memory storage with planned PostgreSQL integration

### Database Layer
- **ORM**: Drizzle ORM for type-safe database operations
- **Database**: PostgreSQL (configured via Neon serverless)
- **Migrations**: Drizzle Kit for schema management
- **Connection**: Environment-based DATABASE_URL configuration

## Key Components

### Document Management System
- **Upload Processing**: Multi-format file support (PDF, Word, Excel, PowerPoint)
- **Storage Strategy**: File metadata stored in database, content in memory (temporary)
- **Module Categorization**: Documents organized by type (RFP, SOW, Procurement)
- **Audit Trail**: Complete tracking of document lifecycle events

### AI Document Generation
- **Template System**: Structured forms for each document type
- **RAG Configuration**: Retrieval-Augmented Generation settings per module
- **Content Generation**: AI-powered document creation based on uploaded references
- **Review Workflow**: Approval/rejection system for generated documents

### Security & Compliance
- **Government Standards**: Tailored UI with official color schemes and styling
- **Audit Logging**: Comprehensive tracking of all user actions
- **Session Security**: Secure session management with user authentication
- **Data Validation**: Strict input validation using Zod schemas

### User Interface Design
- **Responsive Design**: Mobile-first approach with desktop optimization
- **Accessibility**: WCAG-compliant components via Radix UI
- **Government Aesthetics**: Professional styling with neutral color palette
- **Module Navigation**: Tab-based interface for different document types

## Data Flow

1. **Document Upload Flow**:
   - User selects module type and uploads reference documents
   - Files processed through Multer middleware
   - Metadata stored in database, audit entry created
   - Documents available for AI reference during generation

2. **Generation Flow**:
   - User fills module-specific forms with project requirements
   - Form data validated against Zod schemas
   - AI generation triggered with form data and reference documents
   - Generated content stored with pending status
   - Review workflow initiated for approval process

3. **Audit Flow**:
   - All user actions automatically logged
   - Audit entries include timestamps, user context, and action details
   - Analytics dashboard aggregates audit data for reporting
   - Complete traceability of document lifecycle

## External Dependencies

### Core Dependencies
- **@neondatabase/serverless**: Serverless PostgreSQL connection
- **drizzle-orm**: Type-safe ORM for database operations
- **@tanstack/react-query**: Server state management and caching
- **@radix-ui/react-***: Accessible UI component primitives
- **react-hook-form**: Performant form handling
- **zod**: Runtime type validation and schema definition

### Development Tools
- **Vite**: Fast build tool with HMR support
- **TypeScript**: Static type checking across the stack
- **Tailwind CSS**: Utility-first styling framework
- **ESBuild**: Fast bundling for production builds

### File Processing
- **Multer**: Multipart form data handling for file uploads
- **File Type Support**: PDF, Word, Excel, PowerPoint document processing

## Deployment Strategy

### Development Environment
- **Local Development**: Vite dev server with Express API proxy
- **Hot Module Replacement**: Real-time updates during development
- **Environment Variables**: DATABASE_URL for database connection
- **Replit Integration**: Optimized for Replit development environment

### Production Build
- **Client Build**: Vite builds React app to `dist/public`
- **Server Build**: ESBuild bundles Express server to `dist/index.js`
- **Asset Handling**: Static file serving in production mode
- **Database Setup**: Drizzle migrations via `npm run db:push`

### Database Management
- **Schema Definition**: Centralized in `shared/schema.ts`
- **Migrations**: Automated via Drizzle Kit
- **Connection Pooling**: Handled by Neon serverless driver
- **Type Safety**: Full TypeScript integration with database schema

## Changelog
- July 01, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.